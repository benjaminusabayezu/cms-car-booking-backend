from rest_framework import viewsets, status
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated, AllowAny
from apps.authentication.permissions import IsManagerUserRole, IsClientUserRole
from .models import Car, Booking
from .serializers import CarSerializer, BookingSerializer

class CarViewSet(viewsets.ModelViewSet):
    """
    Manage Car Inventory:
    - Public: Can view available cars.
    - Managers/Admins: Full CRUD access.
    """
    queryset = Car.objects.all()
    serializer_class = CarSerializer

    def get_permissions(self):
        if self.action in ['list', 'retrieve']:
            return [AllowAny()]
        return [IsManagerUserRole()]


class BookingViewSet(viewsets.ModelViewSet):
    """
    Manage Reservations:
    - Clients: View personal history, create bookings, cancel pending bookings.
    - Managers/Admins: Complete oversight of all bookings.
    """
    serializer_class = BookingSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        # Admins & Managers see all reservations across the board
        if user.role in ['ADMIN', 'MANAGER']:
            return Booking.objects.all().order_by('-created_at')
        # Clients can only view their own bookings
        return Booking.objects.filter(client=user).order_by('-created_at')

    def perform_create(self, serializer):
        # Automatically assign the request user as the client
        serializer.save(client=self.request.user)

    def destroy(self, request, *args, **kwargs):
        """Standard cancel logic."""
        booking = self.get_object()
        
        # Clients can only cancel their own booking if it hasn't been completed
        if request.user.role == 'CLIENT':
            if booking.client != request.user:
                return Response({"detail": "Unauthorized."}, status=status.HTTP_403_FORBIDDEN)
            if booking.status in ['CONFIRMED', 'COMPLETED']:
                return Response(
                    {"detail": "Active or completed bookings cannot be deleted. Please contact a manager."}, 
                    status=status.HTTP_400_BAD_REQUEST
                )
        
        booking.status = 'CANCELLED'
        booking.save()
        return Response({"status": "Booking successfully cancelled."}, status=status.HTTP_200_OK)