from rest_framework import serializers
from .models import FormTemplate, FormField, FormSubmission


class FormFieldSerializer(serializers.ModelSerializer):
    class Meta:
        model = FormField
        fields = [
            "id",
            "label",
            "key",
            "field_type",
            "is_required",
            "placeholder",
            "help_text",
            "options",
            "sort_order",
            "is_active",
        ]


class FormTemplateSerializer(serializers.ModelSerializer):
    fields = FormFieldSerializer(many=True, read_only=True)

    class Meta:
        model = FormTemplate
        fields = [
            "id",
            "title",
            "slug",
            "description",
            "status",
            "fields",
            "created_at",
            "updated_at",
        ]


class FormSubmissionCreateSerializer(serializers.Serializer):
    form_slug = serializers.CharField()
    wallet_address = serializers.CharField(required=False, allow_blank=True, allow_null=True)
    submitted_data = serializers.JSONField()

    def validate(self, attrs):
        form_slug = attrs.get("form_slug")
        submitted_data = attrs.get("submitted_data")

        try:
            form = FormTemplate.objects.get(slug=form_slug, status="ACTIVE")
        except FormTemplate.DoesNotExist:
            raise serializers.ValidationError({"form_slug": "Active form not found."})

        active_fields = form.fields.filter(is_active=True)

        allowed_keys = [field.key for field in active_fields]
        required_keys = [field.key for field in active_fields if field.is_required]

        for key in required_keys:
            value = submitted_data.get(key)
            if value in [None, ""]:
                raise serializers.ValidationError({key: "This field is required."})

        for key in submitted_data.keys():
            if key not in allowed_keys:
                raise serializers.ValidationError({key: "This field is not allowed for this form."})

        attrs["form"] = form
        return attrs


class FormSubmissionSerializer(serializers.ModelSerializer):
    form_title = serializers.CharField(source="form.title", read_only=True)
    form_slug = serializers.CharField(source="form.slug", read_only=True)

    class Meta:
        model = FormSubmission
        fields = [
            "id",
            "submission_ref",
            "form",
            "form_title",
            "form_slug",
            "wallet_address",
            "submitted_data",
            "data_hash",
            "blockchain_tx_hash",
            "blockchain_status",
            "verification_status",
            "status",
            "ip_address",
            "created_at",
            "updated_at",
        ]
        read_only_fields = fields