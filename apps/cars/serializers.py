from rest_framework import serializers
from django.utils import timezone
from .models import Car, Booking

class CarSerializer(serializers.ModelSerializer):
    class Meta:
        model = Car
        fields = '__all__'


class BookingSerializer(serializers.ModelSerializer):
    client_email = serializers.EmailField(source='client.email', read_only=True)
    car_details = CarSerializer(source='car', read_only=True)
    total_price = serializers.DecimalField(max_digits=10, decimal_places=2, read_only=True)

    class Meta:
        model = Booking
        fields = [
            'id', 'client', 'client_email', 'car', 'car_details', 
            'start_date', 'end_date', 'status', 'total_price', 'created_at'
        ]
        # Keep clients from writing their own total prices or force-approving their status
        read_only_fields = ['client', 'status', 'total_price', 'created_at']

def validate(self, attrs):
    start_date = attrs.get("start_date")
    end_date = attrs.get("end_date")
    car = attrs.get("car")

    # For PATCH updates, use existing values
    if self.instance:
        start_date = start_date or self.instance.start_date
        end_date = end_date or self.instance.end_date
        car = car or self.instance.car

    # 1. Basic sanity date checking
    if start_date < timezone.now().date():
        raise serializers.ValidationError({
            "start_date": "Booking start date cannot be in the past."
        })

    if end_date <= start_date:
        raise serializers.ValidationError({
            "end_date": "End date must fall after the start date."
        })

    # 2. Check vehicle availability
    if not car.is_available:
        raise serializers.ValidationError({
            "car": "This vehicle is currently undergoing maintenance."
        })

    # 3. Check overlapping reservations
    booking_id = self.instance.id if self.instance else None

    overlapping_bookings = Booking.objects.filter(
        car=car,
        status__in=["PENDING", "CONFIRMED"],
        start_date__lt=end_date,
        end_date__gt=start_date
    )

    if booking_id:
        overlapping_bookings = overlapping_bookings.exclude(
            id=booking_id
        )

    if overlapping_bookings.exists():
        raise serializers.ValidationError({
            "non_field_errors":
            "This vehicle is already reserved or pending reservation during these dates."
        })

    return attrs