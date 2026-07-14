from django.contrib import admin

from .models import Car, Booking
# Register your models here.


@admin.register(Car)
class CarAdmin(admin.ModelAdmin):
    list_display = ('brand', 'model_name', 'year', 'price_per_day', 'is_available')
    list_filter = ('is_available', 'year')
    search_fields = ('brand', 'model_name', 'licence_plate')
    list_editable = ('is_available', 'price_per_day')
    
    # Organize fields on edit screen
    fieldsets = (
        ('Vehicle Specs', {
            'fields': ('brand', 'model_name', 'year', 'licence_plate')
        }),
        ('Pricing & Status', {
            'fields': ('price_per_day', 'is_available')
        }),
        ('Media Assets', {
            'fields': ('image',),
            'description': 'Upload clear high-res photos for landing page rendering.'
        }),
    )


@admin.register(Booking)
class BookingAdmin(admin.ModelAdmin):
    list_display = ('id', 'client', 'car', 'start_date', 'end_date', 'total_price', 'status')
    list_filter = ('status', 'start_date', 'end_date')
    search_fields = ('user__email', 'user__first_name', 'car__brand', 'car__model')
    
    # Lock important financial calculation fields to read-only to avoid unauthorized modifications
    readonly_fields = ('total_price', 'created_at')
    
    actions = ['mark_as_approved', 'mark_as_completed']

    # Custom Admin Actions!
    @admin.action(description="Approve selected bookings")
    def mark_as_approved(self, request, queryset):
        updated = queryset.update(status='APPROVED')
        self.message_user(request, f"{updated} bookings have been approved.")

    @admin.action(description="Mark selected bookings as Completed")
    def mark_as_completed(self, request, queryset):
        updated = queryset.update(status='COMPLETED')
        self.message_user(request, f"{updated} bookings were marked completed.")