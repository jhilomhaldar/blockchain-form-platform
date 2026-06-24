import uuid
from django.db import models
from django.utils import timezone


class FormTemplate(models.Model):
    STATUS_CHOICES = (
        ("ACTIVE", "Active"),
        ("INACTIVE", "Inactive"),
    )

    title = models.CharField(max_length=255)
    slug = models.SlugField(max_length=255, unique=True)
    description = models.TextField(blank=True, null=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default="ACTIVE")
    created_at = models.DateTimeField(default=timezone.now)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = "form_templates"
        ordering = ["-created_at"]

    def __str__(self):
        return self.title


class FormField(models.Model):
    FIELD_TYPE_CHOICES = (
        ("TEXT", "Text"),
        ("EMAIL", "Email"),
        ("PHONE", "Phone"),
        ("NUMBER", "Number"),
        ("TEXTAREA", "Textarea"),
        ("SELECT", "Select"),
        ("CHECKBOX", "Checkbox"),
        ("RADIO", "Radio"),
        ("DATE", "Date"),
    )

    form = models.ForeignKey(
        FormTemplate,
        related_name="fields",
        on_delete=models.CASCADE
    )
    label = models.CharField(max_length=255)
    key = models.SlugField(max_length=255)
    field_type = models.CharField(max_length=30, choices=FIELD_TYPE_CHOICES, default="TEXT")
    is_required = models.BooleanField(default=False)
    placeholder = models.CharField(max_length=255, blank=True, null=True)
    help_text = models.CharField(max_length=255, blank=True, null=True)
    options = models.JSONField(default=list, blank=True)
    sort_order = models.PositiveIntegerField(default=0)
    is_active = models.BooleanField(default=True)

    class Meta:
        db_table = "form_fields"
        ordering = ["sort_order", "id"]
        unique_together = ("form", "key")

    def __str__(self):
        return f"{self.form.title} - {self.label}"


class FormSubmission(models.Model):
    STATUS_CHOICES = (
        ("PENDING", "Pending"),
        ("HASHED", "Hashed"),
        ("BLOCKCHAIN_PENDING", "Blockchain Pending"),
        ("BLOCKCHAIN_CONFIRMED", "Blockchain Confirmed"),
        ("VERIFIED", "Verified"),
        ("FAILED", "Failed"),
        ("REJECTED", "Rejected"),
    )

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    submission_ref = models.CharField(max_length=50, unique=True, db_index=True)
    form = models.ForeignKey(
        FormTemplate,
        related_name="submissions",
        on_delete=models.PROTECT
    )

    wallet_address = models.CharField(max_length=100, blank=True, null=True)

    submitted_data = models.JSONField(default=dict)
    data_hash = models.CharField(max_length=66, db_index=True)

    blockchain_tx_hash = models.CharField(max_length=100, blank=True, null=True)
    blockchain_status = models.CharField(max_length=50, default="NOT_SUBMITTED")

    verification_status = models.CharField(max_length=50, default="NOT_VERIFIED")
    status = models.CharField(max_length=40, choices=STATUS_CHOICES, default="HASHED")

    ip_address = models.GenericIPAddressField(blank=True, null=True)
    user_agent = models.TextField(blank=True, null=True)

    created_at = models.DateTimeField(default=timezone.now)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = "form_submissions"
        ordering = ["-created_at"]

    def __str__(self):
        return self.submission_ref


class BlockchainTransaction(models.Model):
    STATUS_CHOICES = (
        ("PENDING", "Pending"),
        ("CONFIRMED", "Confirmed"),
        ("FAILED", "Failed"),
    )

    submission = models.OneToOneField(
        FormSubmission,
        related_name="blockchain_transaction",
        on_delete=models.CASCADE
    )
    network = models.CharField(max_length=100, default="LOCAL_HARDHAT")
    contract_address = models.CharField(max_length=100, blank=True, null=True)
    tx_hash = models.CharField(max_length=100, blank=True, null=True)
    block_number = models.BigIntegerField(blank=True, null=True)
    gas_used = models.BigIntegerField(blank=True, null=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default="PENDING")
    error_message = models.TextField(blank=True, null=True)

    created_at = models.DateTimeField(default=timezone.now)
    confirmed_at = models.DateTimeField(blank=True, null=True)

    class Meta:
        db_table = "blockchain_transactions"
        ordering = ["-created_at"]

    def __str__(self):
        return f"{self.submission.submission_ref} - {self.status}"


class VerificationLog(models.Model):
    RESULT_CHOICES = (
        ("MATCHED", "Matched"),
        ("MISMATCHED", "Mismatched"),
        ("NOT_FOUND", "Not Found"),
        ("ERROR", "Error"),
    )

    submission = models.ForeignKey(
        FormSubmission,
        related_name="verification_logs",
        on_delete=models.CASCADE
    )
    database_hash = models.CharField(max_length=66)
    blockchain_hash = models.CharField(max_length=66, blank=True, null=True)
    result = models.CharField(max_length=30, choices=RESULT_CHOICES)
    checked_at = models.DateTimeField(default=timezone.now)
    checked_by_ip = models.GenericIPAddressField(blank=True, null=True)

    class Meta:
        db_table = "verification_logs"
        ordering = ["-checked_at"]

    def __str__(self):
        return f"{self.submission.submission_ref} - {self.result}"