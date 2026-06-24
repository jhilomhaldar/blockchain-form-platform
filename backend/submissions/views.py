from django.db import transaction
from django.utils import timezone
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

from .models import FormTemplate, FormSubmission, VerificationLog
from .serializers import (
    FormTemplateSerializer,
    FormSubmissionCreateSerializer,
    FormSubmissionSerializer,
)
from .services.hash_service import generate_submission_hash

from .services.blockchain_service import (
    submit_proof_to_blockchain,
    verify_proof_on_blockchain,
)

def get_client_ip(request):
    forwarded_for = request.META.get("HTTP_X_FORWARDED_FOR")
    if forwarded_for:
        return forwarded_for.split(",")[0].strip()
    return request.META.get("REMOTE_ADDR")


def generate_submission_ref():
    today = timezone.now().strftime("%Y%m%d")
    prefix = f"SUB-{today}"

    last_submission = (
        FormSubmission.objects
        .filter(submission_ref__startswith=prefix)
        .order_by("-created_at")
        .first()
    )

    if not last_submission:
        next_number = 1
    else:
        try:
            last_number = int(last_submission.submission_ref.split("-")[-1])
            next_number = last_number + 1
        except ValueError:
            next_number = 1

    return f"{prefix}-{next_number:06d}"


class FormTemplateListAPIView(APIView):
    def get(self, request):
        forms = FormTemplate.objects.filter(status="ACTIVE")
        serializer = FormTemplateSerializer(forms, many=True)
        return Response({
            "success": True,
            "data": serializer.data
        })


class FormTemplateDetailAPIView(APIView):
    def get(self, request, slug):
        try:
            form = FormTemplate.objects.get(slug=slug, status="ACTIVE")
        except FormTemplate.DoesNotExist:
            return Response({
                "success": False,
                "message": "Form not found."
            }, status=status.HTTP_404_NOT_FOUND)

        serializer = FormTemplateSerializer(form)
        return Response({
            "success": True,
            "data": serializer.data
        })


class FormSubmissionCreateAPIView(APIView):
    @transaction.atomic
    def post(self, request):
        serializer = FormSubmissionCreateSerializer(data=request.data)

        if not serializer.is_valid():
            return Response({
                "success": False,
                "errors": serializer.errors
            }, status=status.HTTP_400_BAD_REQUEST)

        form = serializer.validated_data["form"]
        submitted_data = serializer.validated_data["submitted_data"]
        wallet_address = serializer.validated_data.get("wallet_address")

        data_hash = generate_submission_hash(submitted_data)
        submission_ref = generate_submission_ref()

        submission = FormSubmission.objects.create(
            submission_ref=submission_ref,
            form=form,
            wallet_address=wallet_address,
            submitted_data=submitted_data,
            data_hash=data_hash,
            ip_address=get_client_ip(request),
            user_agent=request.META.get("HTTP_USER_AGENT", ""),
            status="HASHED",
            blockchain_status="NOT_SUBMITTED",
            verification_status="NOT_VERIFIED",
        )

        blockchain_result = submit_proof_to_blockchain(submission)

        submission.refresh_from_db()
        response_serializer = FormSubmissionSerializer(submission)

        return Response({
            "success": True,
            "message": "Form submitted successfully. Hash generated and blockchain proof processed.",
            "data": response_serializer.data,
            "blockchain": blockchain_result
        }, status=status.HTTP_201_CREATED)

        return Response({
            "success": True,
            "message": "Form submitted successfully. Hash generated.",
            "data": response_serializer.data
        }, status=status.HTTP_201_CREATED)


class FormSubmissionDetailAPIView(APIView):
    def get(self, request, submission_ref):
        try:
            submission = FormSubmission.objects.get(submission_ref=submission_ref)
        except FormSubmission.DoesNotExist:
            return Response({
                "success": False,
                "message": "Submission not found."
            }, status=status.HTTP_404_NOT_FOUND)

        serializer = FormSubmissionSerializer(submission)
        return Response({
            "success": True,
            "data": serializer.data
        })


class FormSubmissionVerifyAPIView(APIView):
    def get(self, request, submission_ref):
        try:
            submission = FormSubmission.objects.get(submission_ref=submission_ref)
        except FormSubmission.DoesNotExist:
            return Response({
                "success": False,
                "message": "Submission not found."
            }, status=status.HTTP_404_NOT_FOUND)

        regenerated_hash = generate_submission_hash(submission.submitted_data)
        database_verified = regenerated_hash == submission.data_hash

        blockchain_result = verify_proof_on_blockchain(submission)

        blockchain_verified = blockchain_result.get("verified", False)
        final_verified = database_verified and blockchain_verified

        submission.verification_status = "VERIFIED" if final_verified else "FAILED"
        submission.save(update_fields=["verification_status", "updated_at"])

        VerificationLog.objects.create(
            submission=submission,
            database_hash=regenerated_hash,
            blockchain_hash=blockchain_result.get("blockchain_hash"),
            result="MATCHED" if final_verified else "MISMATCHED",
            checked_by_ip=get_client_ip(request),
        )

        return Response({
            "success": True,
            "submission_ref": submission.submission_ref,
            "database": {
                "stored_hash": submission.data_hash,
                "regenerated_hash": regenerated_hash,
                "verified": database_verified,
            },
            "blockchain": blockchain_result,
            "verified": final_verified,
        })