from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import CustomUser


@admin.register(CustomUser)
class CustomUserAdmin(UserAdmin):
    model = CustomUser

    list_display = (
        "email",
        "username",
        "role",
        "phone_number",
        "is_staff",
        "is_active",
    )

    list_filter = (
        "role",
        "is_staff",
        "is_active",
        "date_joined",
    )

    list_editable = (
        "role",
        "is_active",
    )

    search_fields = (
        "email",
        "username",
        "phone_number",
    )

    ordering = ("-date_joined",)

    fieldsets = (
        (None, {
            "fields": (
                "email",
                "username",
                "password",
            )
        }),
        ("Personal Info", {
            "fields": (
                "first_name",
                "last_name",
                "phone_number",
            )
        }),
        ("Permissions", {
            "fields": (
                "role",
                "is_active",
                "is_staff",
                "is_superuser",
                "groups",
                "user_permissions",
            )
        }),
        ("Important Dates", {
            "fields": (
                "last_login",
                "date_joined",
            )
        }),
    )

    add_fieldsets = (
        (None, {
            "classes": ("wide",),
            "fields": (
                "email",
                "username",
                "role",
                "phone_number",
                "password1",
                "password2",
            ),
        }),
    )