from django.shortcuts import render
from rest_framework import generics, status
from rest_framework.response import Response
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework.views import APIView

# Mail & Token Utilities for Reset Password
from django.contrib.auth.tokens import PasswordResetTokenGenerator
from django.utils.encoding import force_bytes
from django.utils.http import urlsafe_base64_encode
from django.core.mail import send_mail
from django.conf import settings

from .models import CustomUser
from .serializers import (
    CustomTokenObtainPairSerializer,
    UserRegisterSerializer,
    ChangePasswordSerializer,
    ForgotPasswordSerializer,
    ResetPasswordSerializer,
)


class CustomTokenObtainPairView(TokenObtainPairView):
    """Login view to use customized token payload."""
    serializer_class = CustomTokenObtainPairSerializer


class UserRegisterView(generics.CreateAPIView):
    """Public endpoint for new clients to create accounts."""
    queryset = CustomUser.objects.all()
    serializer_class = UserRegisterSerializer
    permission_classes = [AllowAny]


class ChangePasswordView(APIView):
    """Allows logged-in users to update their password."""
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]

    def post(self, request):
        serializer = ChangePasswordSerializer(data=request.data, context={'request': request})
        serializer.is_valid(raise_exception=True)

        # FIXED TYPO: validated_data (was validate_data)
        request.user.set_password(serializer.validated_data['new_password'])
        request.user.save()

        return Response(
            {"message": "Password updated successfully."},
            status=status.HTTP_200_OK
        )


class ForgotPasswordView(APIView):
    """Sends a password reset link to the user's email."""
    permission_classes = [AllowAny]

    def post(self, request):
        serializer = ForgotPasswordSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        email = serializer.validated_data['email']

        try:
            user = CustomUser.objects.get(email=email)
            token = PasswordResetTokenGenerator().make_token(user)
            uidb64 = urlsafe_base64_encode(force_bytes(user.pk))

            # Point this to your frontend route that accepts token & uidb64
            reset_link = f"https://yourfrontend.com/reset-password/{uidb64}/{token}/"

            send_mail(
                subject="Password Reset Request",
                message=f"Hi,\n\nUse the link below to reset your password:\n{reset_link}\n\nIf you did not request this, please ignore this email.",
                from_email=getattr(settings, 'DEFAULT_FROM_EMAIL', 'noreply@localhost'),
                recipient_list=[user.email],
                fail_silently=False,
            )
        except CustomUser.DoesNotExist:
            # Prevents email enumeration / user fishing attacks
            pass

        return Response(
            {"message": "If an account with that email exists, a password reset link has been sent."},
            status=status.HTTP_200_OK
        )


class ResetPasswordView(APIView):
    """Resets the password using token and uidb64 from the email link."""
    permission_classes = [AllowAny]

    def post(self, request):
        serializer = ResetPasswordSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        user = serializer.validated_data['user']
        user.set_password(serializer.validated_data['password'])
        user.save()

        return Response(
            {"message": "Password reset successful. You can now log in with your new password."},
            status=status.HTTP_200_OK
        )