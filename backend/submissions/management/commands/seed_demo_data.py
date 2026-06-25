from django.core.management.base import BaseCommand
from django.db import transaction

from submissions.models import FormTemplate, FormField


class Command(BaseCommand):
    help = "Seed demo form template and fields for local project setup."

    @transaction.atomic
    def handle(self, *args, **options):
        form, created = FormTemplate.objects.update_or_create(
            slug="contact-verification-form",
            defaults={
                "title": "Contact Verification Form",
                "description": "A sample blockchain-ready contact form for secure submission verification.",
                "status": "ACTIVE",
            },
        )

        fields = [
            {
                "label": "Name",
                "key": "name",
                "field_type": "TEXT",
                "is_required": True,
                "placeholder": "Enter your Name",
                "help_text": "",
                "options": [],
                "sort_order": 1,
                "is_active": True,
            },
            {
                "label": "Email",
                "key": "email",
                "field_type": "EMAIL",
                "is_required": True,
                "placeholder": "Enter your Email",
                "help_text": "",
                "options": [],
                "sort_order": 2,
                "is_active": True,
            },
            {
                "label": "Phone",
                "key": "phone",
                "field_type": "PHONE",
                "is_required": False,
                "placeholder": "Enter your Phone",
                "help_text": "",
                "options": [],
                "sort_order": 3,
                "is_active": True,
            },
            {
                "label": "Message",
                "key": "message",
                "field_type": "TEXTAREA",
                "is_required": False,
                "placeholder": "Enter Message",
                "help_text": "",
                "options": [],
                "sort_order": 4,
                "is_active": True,
            },
        ]

        for field_data in fields:
            FormField.objects.update_or_create(
                form=form,
                key=field_data["key"],
                defaults=field_data,
            )

        self.stdout.write(
            self.style.SUCCESS(
                "Demo data seeded successfully: Contact Verification Form created/updated."
            )
        )

        self.stdout.write(
            self.style.SUCCESS(
                "Open frontend: http://localhost:5173/forms/contact-verification-form"
            )
        )