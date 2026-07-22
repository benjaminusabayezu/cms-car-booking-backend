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
                "ADMIN_EMAIL or ADMIN_PASSWORD not set"
            )
            return

        if not User.objects.filter(email=email).exists():

            user = User.objects.create_superuser(
                email=email,
                password=password
            )

            self.stdout.write(
                self.style.SUCCESS(
                    f"Admin created: {user.email}"
                )
            )

        else:
            self.stdout.write(
                "Admin already exists"
            )