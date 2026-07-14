from django.contrib import admin

from .models import LandingPageConfig, NavbarLink
# Register your models here.

@admin.register(LandingPageConfig)
class LandingPageAdmin(admin.ModelAdmin):
    list_display = ('site_name', 'contact_email', 'contact_phone', 'updated_at')
    fieldsets = (
        ('General Branding', {
            'fields': ('site_name',)
        }),
        ('Hero Section Copy', {
            'fields': ('hero_title', 'hero_subtitle', 'hero_cta_text','hero_image'),
            'description': 'Configure the main text blocks on your frontend landing page hero unit.'
        }),
        ('Contact Information', {
            'fields': ('contact_email', 'contact_phone', 'copyright_text')
        }),
    )

    # Singleton Guard: Prevent adding a new record if one already exists
    def has_add_permission(self, request):
        if self.model.objects.exists():
            return False
        return super().has_add_permission(request)

    # Prevent deleting the core configuration setup
    def has_delete_permission(self, request, obj=None):
        return False


@admin.register(NavbarLink)
class NavbarLinkAdmin(admin.ModelAdmin):
    # What shows up in the admin table list
    list_display = ('label', 'url_path', 'order', 'is_active')
    # Make fields editable directly inside the list table!
    list_editable = ('order', 'url_path', 'is_active')
    ordering = ('order',)
    search_fields = ('label', 'url_path')