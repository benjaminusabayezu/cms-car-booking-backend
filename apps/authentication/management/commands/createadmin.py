from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model
import os


class Command(BaseCommand):
    help = "Create default admin user"

    def handle(self, *args, **kwargs):

        User = get_user_model()

        email = os.environ.get("ADMIN_EMAIL")
        password = os.environ.get("ADMIN_PASSWORD")

        if not email or not password:
            self.stdout.write(
                self.style.ERROR(
                    "ADMIN_EMAIL or ADMIN_PASSWORD not set"
                )
            )
            return

        if User.objects.filter(email=email).exists():
            self.stdout.write(
                self.style.WARNING(
                    "Admin already exists"
                )
            )
            return

        user = User.objects.create_superuser(
            username=email,
            email=email,
            password=password,
            role="admin"
        )

        self.stdout.write(
            self.style.SUCCESS(
                f"Admin created successfully: {user.email}"
            )
        )