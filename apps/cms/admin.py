from django.contrib import admin

from .models import (
    LandingPageConfig,
      NavbarLink,
      CompanyInformation,
      FooterConfig,
      Service,
      Feature,
      FAQ,
      Testimonial, SocialLink
)
# Register your models here.
class SingletonAdminMixin:
    def has_add_permission(self, request):
        if self.model.objects.exists():
            return False
        return super().has_add_permission(request)

    def has_delete_permission(self, request, obj=None):
        return False

@admin.register(LandingPageConfig)
class LandingPageAdmin(SingletonAdminMixin,admin.ModelAdmin):
    list_display = ('site_name', 'contact_email', 'contact_phone', 'updated_at')
    fieldsets = (
        ('General Branding', {
            'fields': ('site_name',)
        }),
        ('Hero Section Copy', {
            'fields': ('hero_title', 'hero_subtitle', 'hero_cta_text','hero_image'),
            'description': 'Configure the main text blocks on your frontend landing page hero unit.'
        }),

    )

@admin.register(CompanyInformation)
class CompanyInformationAdmin(SingletonAdminMixin, admin.ModelAdmin):
    list_display = ('contact_email', 'contact_phone')
    fieldsets = (
        ('Primary Contact Details', {
            'fields': ('contact_email', 'contact_phone', 'address')
        }),
        ('Meta Details', {
            'fields': ('about_us_short',),
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


@admin.register(FooterConfig)
class FooterConfigAdmin(SingletonAdminMixin, admin.ModelAdmin):
    list_display = ('copyright_text',)


@admin.register(Service)
class ServiceAdmin(admin.ModelAdmin):
    list_display = ('title', 'icon_name', 'order')
    list_editable = ('order',)


@admin.register(Feature)
class FeatureAdmin(admin.ModelAdmin):
    list_display = ('title', 'order')
    list_editable = ('order',)


@admin.register(FAQ)
class FAQAdmin(admin.ModelAdmin):
    list_display = ('question', 'order')
    list_editable = ('order',)


@admin.register(Testimonial)
class TestimonialAdmin(admin.ModelAdmin):
    list_display = ('client_name', 'client_role', 'rating')


@admin.register(SocialLink)
class SocialLinkAdmin(admin.ModelAdmin):
    list_display = ('platform', 'url', 'is_active')
    list_filter = ('is_active',)

@admin.register(NavbarLink)
class NavbarLinkAdmin(admin.ModelAdmin):
    # What shows up in the admin table list
    list_display = ('label', 'url_path', 'order', 'is_active')
    # Make fields editable directly inside the list table!
    list_editable = ('order', 'url_path', 'is_active')
    ordering = ('order',)
    search_fields = ('label', 'url_path')