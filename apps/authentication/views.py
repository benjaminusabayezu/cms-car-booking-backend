from django.shortcuts import render
from rest_framework import generics, status, permissions
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
    # Make sure to define/import these three in serializers.py:
    UserSerializer,
    UserCreateSerializer,
    UserRoleSerializer,
    UserProfileSerializer,
    SystemSettingsSerializer,
)


# ==========================================
# Custom Permissions
# ==========================================

class IsAdminOrSuperAdmin(permissions.BasePermission):
    """
    Ensures only users with ADMIN or SUPERADMIN roles can manage users.
    """
    def has_permission(self, request, view):
        return (
            request.user 
            and request.user.is_authenticated 
            and getattr(request.user, 'role', None) in ['ADMIN', 'SUPERADMIN']
        )


# ==========================================
# User Management Views (Dashboard)
# ==========================================

class UserListView(generics.ListCreateAPIView):
    """
    GET /api/auth/users/  -> Returns a list of all registered users.
    POST /api/auth/users/ -> Provisions a new user account.
    """
    queryset = CustomUser.objects.all().order_by('-id')
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAdminOrSuperAdmin]

    def get_serializer_class(self):
        if self.request.method == 'POST':
            return UserCreateSerializer
        return UserSerializer


class UserRoleUpdateView(generics.UpdateAPIView):
    """
    PATCH /api/auth/users/<id>/role/ -> Updates a specific user's access role.
    """
    queryset = CustomUser.objects.all()
    serializer_class = UserRoleSerializer
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAdminOrSuperAdmin]

    def patch(self, request, *args, **kwargs):
        target_user = self.get_object()

        # Security check: Prevent self-demotion or self-role edits
        if target_user.id == request.user.id:
            return Response(
                {"detail": "You cannot modify your own role clearance level."},
                status=status.HTTP_400_BAD_REQUEST
            )

        return super().patch(request, *args, **kwargs)


# ==========================================
# Existing Authentication & Account Views
# ==========================================

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

            reset_link = f"http://localhost:5173/reset-password/{uidb64}/{token}/"

            send_mail(
                subject="Password Reset Request",
                message=f"Hi,\n\nUse the link below to reset your password:\n{reset_link}\n\nIf you did not request this, please ignore this email.",
                from_email=getattr(settings, 'DEFAULT_FROM_EMAIL', 'noreply@localhost'),
                recipient_list=[user.email],
                fail_silently=False,
            )
        except CustomUser.DoesNotExist:
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
    
class UserProfileView(generics.RetrieveUpdateAPIView):
   """
    GET /api/auth/profile/ -Fetch logged-in user profile details
    PUT/PATCH /api/auth/profile/ - Update logged-in user profile details
    """
   serializer_class = UserProfileSerializer
   authentication_classes = [JWTAuthentication]
   permission_classes = [IsAuthenticated]

   def get_object(self):
        return self.request.user

class UserSettingsView(generics.GenericAPIView):
     """
    GET /api/auth/settings/  -> Fetch current user settings/preferences
    POST /api/auth/settings/ -> Update user settings/preferences
    """
     serializer_class = SystemSettingsSerializer
     authentication_class = [JWTAuthentication]
     permission_classes =[IsAuthenticated]

     def get(self, request):
         #defaultsetting state.
         settings_data ={
             "notifications_enabled":True,
             "email_alerts":True,
             "theme_preference": "light"
         }
         return Response(settings_data, status = status.HTTP_200_OK)
     def post(self, request):
        serializer = self.get_serializer(data = request.data)
        serializer.is_valid(raise_exception = True)
        return Response({"Message" :"Settings Updated Successfully.","data": serializer.validated_data},status = status.HTTP_200_OK)
     
    