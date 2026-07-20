from rest_framework import viewsets, status
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.exceptions import PermissionDenied
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

    Clients:
    - View their own booking history
    - Create bookings
    - Cancel pending bookings

    Managers/Admins:
    - View all bookings
    - Confirm bookings
    - Complete bookings
    - Cancel bookings
    """

    serializer_class = BookingSerializer
    permission_classes = [IsAuthenticated]


    def get_queryset(self):
        user = self.request.user

        # Admins and Managers see everything
        if user.role in ["ADMIN", "MANAGER"]:
            return Booking.objects.all().order_by("-created_at")

        # Clients only see their own bookings
        return Booking.objects.filter(
            client=user
        ).order_by("-created_at")


    def perform_create(self, serializer):
        """
        Automatically attach logged-in user
        as booking client.
        """
        serializer.save(
            client=self.request.user
        )


    def partial_update(self, request, *args, **kwargs):
        """
        PATCH /bookings/{id}/

        Allows:
        - Admin/Manager: update status
        - Client: update normal booking fields only
        """

        booking = self.get_object()

        # If status is being changed
        if "status" in request.data:

            # Only admins/managers allowed
            if request.user.role not in [
                "ADMIN",
                "MANAGER"
            ]:
                return Response(
                    {
                        "detail":
                        "Only managers or admins can update booking status."
                    },
                    status=status.HTTP_403_FORBIDDEN
                )

            new_status = request.data.get("status")

            valid_statuses = [
                "PENDING",
                "CONFIRMED",
                "COMPLETED",
                "CANCELLED",
            ]

            if new_status not in valid_statuses:
                return Response(
                    {
                        "detail":
                        f"Invalid status. Choose from {valid_statuses}"
                    },
                    status=status.HTTP_400_BAD_REQUEST
                )


        return super().partial_update(
            request,
            *args,
            **kwargs
        )


    def destroy(self, request, *args, **kwargs):
        """
        Cancel booking instead of deleting it.
        """

        booking = self.get_object()


        # Client cancellation rules
        if request.user.role == "CLIENT":

            if booking.client != request.user:
                return Response(
                    {
                        "detail":
                        "Unauthorized."
                    },
                    status=status.HTTP_403_FORBIDDEN
                )


            if booking.status in [
                "CONFIRMED",
                "COMPLETED"
            ]:
                return Response(
                    {
                        "detail":
                        "Confirmed or completed bookings cannot be cancelled."
                    },
                    status=status.HTTP_400_BAD_REQUEST
                )


        booking.status = "CANCELLED"
        booking.save()


        return Response(
            {
                "status":
                "Booking successfully cancelled."
            },
            status=status.HTTP_200_OK
        )