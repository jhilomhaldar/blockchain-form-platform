from django.core.management.base import BaseCommand

from submissions.models import FormSubmission
from submissions.services.hash_service import generate_submission_hash
from submissions.services.blockchain_service import (
    verify_proof_on_blockchain,
    submit_proof_to_blockchain,
)


class Command(BaseCommand):
    help = "Re-register existing PostgreSQL submissions into the current local blockchain contract."

    def add_arguments(self, parser):
        parser.add_argument(
            "--ref",
            type=str,
            help="Resync only one submission reference, for example SUB-20260625-000001",
        )

        parser.add_argument(
            "--limit",
            type=int,
            default=100,
            help="Maximum number of submissions to check. Default is 100.",
        )

        parser.add_argument(
            "--dry-run",
            action="store_true",
            help="Check what would be resynced without sending blockchain transactions.",
        )

    def handle(self, *args, **options):
        submission_ref = options.get("ref")
        limit = options.get("limit")
        dry_run = options.get("dry_run")

        queryset = FormSubmission.objects.select_related("form").order_by("created_at")

        if submission_ref:
            queryset = queryset.filter(submission_ref=submission_ref)
        else:
            queryset = queryset[:limit]

        checked = 0
        skipped = 0
        resynced = 0
        failed = 0

        self.stdout.write(self.style.WARNING("Starting blockchain proof resync..."))

        for submission in queryset:
            checked += 1

            self.stdout.write("")
            self.stdout.write(f"Checking: {submission.submission_ref}")

            submitted_data = submission.submitted_data or {}
            regenerated_hash = generate_submission_hash(submitted_data)

            if regenerated_hash != submission.data_hash:
                failed += 1
                self.stdout.write(
                    self.style.ERROR(
                        f"Skipped {submission.submission_ref}: database hash mismatch."
                    )
                )
                continue

            try:
                verification_result = verify_proof_on_blockchain(submission)
                already_verified = bool(verification_result.get("verified"))

                if already_verified:
                    skipped += 1
                    submission.verification_status = "VERIFIED"
                    submission.save(update_fields=["verification_status", "updated_at"])

                    self.stdout.write(
                        self.style.SUCCESS(
                            f"Already valid on current blockchain: {submission.submission_ref}"
                        )
                    )
                    continue

                self.stdout.write(
                    self.style.WARNING(
                        f"Proof missing or invalid on current blockchain: {submission.submission_ref}"
                    )
                )

                if dry_run:
                    self.stdout.write(
                        self.style.WARNING(
                            f"Dry run only. Would resync: {submission.submission_ref}"
                        )
                    )
                    continue

                blockchain_result = submit_proof_to_blockchain(submission)

                if blockchain_result.get("success"):
                    resynced += 1
                    submission.verification_status = "VERIFIED"
                    submission.save(update_fields=["verification_status", "updated_at"])

                    self.stdout.write(
                        self.style.SUCCESS(
                            f"Resynced successfully: {submission.submission_ref}"
                        )
                    )
                    self.stdout.write(f"Tx Hash: {blockchain_result.get('tx_hash')}")
                else:
                    failed += 1
                    self.stdout.write(
                        self.style.ERROR(
                            f"Resync failed for {submission.submission_ref}: {blockchain_result.get('message')}"
                        )
                    )

            except Exception as exc:
                failed += 1
                self.stdout.write(
                    self.style.ERROR(
                        f"Error processing {submission.submission_ref}: {str(exc)}"
                    )
                )

        self.stdout.write("")
        self.stdout.write(self.style.SUCCESS("Blockchain proof resync completed."))
        self.stdout.write(f"Checked: {checked}")
        self.stdout.write(f"Already valid/skipped: {skipped}")
        self.stdout.write(f"Resynced: {resynced}")
        self.stdout.write(f"Failed: {failed}")