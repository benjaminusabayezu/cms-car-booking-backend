from rest_framework import serializers
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from django.contrib.auth.tokens import PasswordResetTokenGenerator
from django.utils.encoding import force_str
from django.utils.http import urlsafe_base64_decode
from .models import CustomUser


# ==========================================
# Dashboard User Management Serializers
# ==========================================

class UserSerializer(serializers.ModelSerializer):
    """Used for listing users in the User Management Dashboard."""
    date_joined = serializers.DateTimeField(format="%Y-%m-%d %H:%M", read_only=True)

    class Meta:
        model = CustomUser
        fields = ['id', 'username', 'email', 'phone_number', 'role', 'date_joined']


class UserCreateSerializer(serializers.ModelSerializer):
    """Used when an administrator creates a new user via the dashboard drawer."""
    password = serializers.CharField(write_only=True, min_length=6)

    class Meta:
        model = CustomUser
        fields = ['id', 'username', 'email', 'password', 'phone_number', 'role']
        extra_kwargs = {
            'username': {'required': False},
            'phone_number': {'required': False},
        }

    def create(self, validated_data):
        # Auto-fallback username to the email prefix if not provided
        email = validated_data['email']
        username = validated_data.get('username') or email.split('@')[0]

        user = CustomUser.objects.create_user(
            username=username,
            email=email,
            password=validated_data['password'],
            phone_number=validated_data.get('phone_number', ''),
            role=validated_data.get('role', 'CLIENT')
        )
        return user


class UserRoleSerializer(serializers.ModelSerializer):
    """Used exclusively for patching role permissions from the dashboard select dropdown."""
    class Meta:
        model = CustomUser
        fields = ['role']


# ==========================================
# Existing Authentication & Account Serializers
# ==========================================

class CustomTokenObtainPairSerializer(TokenObtainPairSerializer):
    """customize jwt to include user roles and profile details"""

    @classmethod
    def get_token(cls, user):
        token = super().get_token(user)

        # add claims to the decrypted token payload
        token['username'] = user.username
        token['email'] = user.email
        token['role'] = user.role

        return token


class UserRegisterSerializer(serializers.ModelSerializer):
    """handle initial client registration."""
    password = serializers.CharField(write_only=True)

    class Meta:
        model = CustomUser
        fields = ['username', 'email', 'password', 'phone_number']

    def create(self, validated_data):
        # client Register publicly
        user = CustomUser.objects.create_user(
            username=validated_data['username'],
            email=validated_data['email'],
            password=validated_data['password'],
            phone_number=validated_data.get('phone_number', ''),
            role='CLIENT'
        )
        return user


# Password management serializers

class ForgotPasswordSerializer(serializers.Serializer):
    """validates the email submitted for password reset."""
    email = serializers.EmailField()


class ResetPasswordSerializer(serializers.Serializer):
    """validate the reset token, uid and updates to new password."""
    password = serializers.CharField(write_only=True, min_length=8)
    uidb64 = serializers.CharField(write_only=True)
    token = serializers.CharField(write_only=True)

    def validate(self, attrs):
        try:
            uid = force_str(urlsafe_base64_decode(attrs.get('uidb64')))
            user = CustomUser.objects.get(pk=uid)
        except (TypeError, ValueError, OverflowError, CustomUser.DoesNotExist):
            raise serializers.ValidationError({"error": "Invalid or expired reset link."})

        if not PasswordResetTokenGenerator().check_token(user, attrs.get('token')):
            raise serializers.ValidationError({"error": "Invalid or expired reset link."})

        attrs['user'] = user
        return attrs


class ChangePasswordSerializer(serializers.Serializer):
    """handles password updates for logged-in users requiring old password confirmation."""
    old_password = serializers.CharField(write_only=True, required=True)
    new_password = serializers.CharField(write_only=True, required=True, min_length=8)

    def validate_old_password(self, value):
        user = self.context['request'].user
        if not user.check_password(value):
            raise serializers.ValidationError("Your current password was entered incorrectly.")
        return value
    

#setting an profile management
class UserProfileSerializer(serializers.ModelSerializer):
    """handle viewing and update the logged in user's profile."""
    date_joined = serializers.DateTimeField(format="%Y-%m-%d %H:%M", read_only= True)

    class Meta:
        model = CustomUser
        fields = ['id','username', 'email','phone_number','role','date_joined']
        read_only_fields = ['id','role','date_joined']

class  SystemSettingsSerializer(serializers.Serializer):
    """handle updates of settings"""
    notifications_enabled = serializers.BooleanField(default=True)
    email_alerts = serializers.BooleanField(default = True)
    theme_preference = serializers.ChoiceField (choices =['dark','light'], default='light')
