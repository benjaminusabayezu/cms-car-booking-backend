from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import CustomUser

# Register your models here.



@admin.register(CustomUser)
class CustomUserAdmin(UserAdmin):
    # 1. Columns displayed in the list/table view
    list_display = ('email', 'username', 'role', 'phone_number', 'is_staff', 'is_active')
    
    # 2. Sidebar filters for quick navigation
    list_filter = ('role', 'is_staff', 'is_active', 'date_joined')
    
    # 3. Quick-edit right from the list view row
    list_editable = ('role', 'is_active')
    
    # 4. Search bar targeting primary descriptors
    search_fields = ('email', 'username', 'phone_number')
    
    # 5. Ordering rules (newest signups first)
    ordering = ('-date_joined',)

    # 6. Structuring fields on the user detail edit screen
    # We extend the base UserAdmin fieldsets to inject role and phone_number cleanly.
    fieldsets = (
        (None, {'fields': ('email', 'username', 'password')}),
        ('Personal Info', {'fields': ('first_name', 'last_name', 'phone_number')}),
        ('Access Levels & Roles', {
            'fields': ('role', 'is_active', 'is_staff', 'is_superuser'),
            'description': 'Manage user groups and global dashboard entry privileges.'
        }),
        ('Important Dates', {'fields': ('last_login', 'date_joined')}),
    )

    # 7. Structure fields when CREATING a new user via the admin dashboard
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'username', 'role', 'phone_number', 'password'),
        }),
    )