from django.contrib import admin
from .models import (
    FormTemplate,
    FormField,
    FormSubmission,
    BlockchainTransaction,
    VerificationLog,
)


class FormFieldInline(admin.TabularInline):
    model = FormField
    extra = 1


@admin.register(FormTemplate)
class FormTemplateAdmin(admin.ModelAdmin):
    list_display = ("title", "slug", "status", "created_at")
    list_filter = ("status",)
    search_fields = ("title", "slug")
    prepopulated_fields = {"slug": ("title",)}
    inlines = [FormFieldInline]


@admin.register(FormSubmission)
class FormSubmissionAdmin(admin.ModelAdmin):
    list_display = (
        "submission_ref",
        "form",
        "wallet_address",
        "status",
        "verification_status",
        "blockchain_status",
        "created_at",
    )
    list_filter = ("status", "verification_status", "blockchain_status", "created_at")
    search_fields = ("submission_ref", "wallet_address", "data_hash")
    readonly_fields = (
        "id",
        "submission_ref",
        "submitted_data",
        "data_hash",
        "ip_address",
        "user_agent",
        "created_at",
        "updated_at",
    )


@admin.register(BlockchainTransaction)
class BlockchainTransactionAdmin(admin.ModelAdmin):
    list_display = ("submission", "network", "status", "tx_hash", "created_at", "confirmed_at")
    list_filter = ("network", "status")
    search_fields = ("tx_hash", "submission__submission_ref")


@admin.register(VerificationLog)
class VerificationLogAdmin(admin.ModelAdmin):
    list_display = ("submission", "result", "checked_at", "checked_by_ip")
    list_filter = ("result", "checked_at")
    search_fields = ("submission__submission_ref", "database_hash", "blockchain_hash")