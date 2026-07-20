from django.db import models
from django.conf import settings
from decimal import Decimal
# Create your models here.

class Car(models.Model):
    brand = models.CharField(max_length=50)
    model_name = models.CharField(max_length=50)
    year = models.PositiveIntegerField()
    licence_plate =models.CharField(max_length=20, unique=True)
    price_per_day = models.DecimalField(max_length=10, decimal_places=2, max_digits=10)
    image =models.ImageField(upload_to='cars_photo/', blank=True, null=True)
    is_available =models.BooleanField(default=True,help_text="Set false if car is under maintenance")

    def __str__(self):
        return f"{self.brand} {self.model_name} {self.year}- {self.licence_plate}"
    
class Booking(models.Model):
    STATUS_CHOICES =(
        ('PENDING','Pending'),
        ('CONFIRMED','Confirmed'),
        ('COMPLETED','Completed'),
        ('CANCELLED','Cancelled'),

    )

    client = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='bookings'
    )
    car = models.ForeignKey(
        Car, on_delete=models.CASCADE,
        related_name='bookings'
    )
    start_date = models.DateField()
    end_date =models.DateField()
    status = models.CharField(max_length=15,choices=STATUS_CHOICES , default='PENDING')
    total_price = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)
    created_at = models.DateField(auto_now_add=True)

    def calculate_total_price(self):
        """calculate price based on days"""
        if self.start_date and  self.end_date:
            days= (self.end_date - self.start_date).days
            
            #charge at least 1 full day if it is 1 day

            days= max(days,1)
            return Decimal(days) * self.car.price_per_day
        return Decimal('0.00')
    def save(self, *args, **kwargs):
        self.total_price = self.calculate_total_price()
        super().save(*args, **kwargs)

    def __str__(self):
        return f"Booking #{self.id} -{self.client.username} {self.car.brand}"