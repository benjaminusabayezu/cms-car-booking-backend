from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model
import os


class Command(BaseCommand):
    help = "Create default admin user or fix existing admin role"


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


        # Check if admin already exists
        existing_user = User.objects.filter(email=email).first()


        if existing_user:

            # Fix old lowercase role
            if existing_user.role != "ADMIN":
                existing_user.role = "ADMIN"
                existing_user.save()

                self.stdout.write(
                    self.style.SUCCESS(
                        f"Existing admin role updated: {existing_user.email}"
                    )
                )
            else:
                self.stdout.write(
                    self.style.WARNING(
                        f"Admin already exists: {existing_user.email}"
                    )
                )

            return


        # Create new admin
        user = User.objects.create_superuser(
            username=email,
            email=email,
            password=password,
            role="ADMIN"
        )


        self.stdout.write(
            self.style.SUCCESS(
                f"Admin created successfully: {user.email}"
            )
        )