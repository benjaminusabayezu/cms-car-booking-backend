from rest_framework import serializers
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from django.contrib.auth.tokens import PasswordResetTokenGenerator
from django.utils.encoding import force_str
from django.utils.http import urlsafe_base64_decode
from .models import CustomUser


class CustomTokenObtainPairSerializer(TokenObtainPairSerializer):
    """customize jwt to include user roles and profile details"""

    @classmethod
    def get_token(cls, user):
        token = super().get_token(user)

        #add claims to the decrypted token payload
        token['username'] = user.username
        token['email'] = user.email
        token ['role'] =user.role

        return token
class UserRegisterSerializer(serializers.ModelSerializer):
    """handle inition client registrtation."""
    password = serializers.CharField(write_only = True)

    class Meta:
        model = CustomUser
        fields =['username','email','password','phone_number']

    def create(self, validated_data):
        #client Register publlically
        user = CustomUser.objects.create_user(
            username= validated_data['username'],
            email= validated_data['email'],
            password=validated_data['password'],
            phone_number = validated_data.get('phone_number', ''),
            role = 'CLIENT'
        )
        return user
    
    #password management serializers.

class ForgotPasswordSerializer(serializers.Serializer):
    """validates the email submitted for password reset.."""
    email = serializers.EmailField()

class ResetPasswordSerializer(serializers.Serializer):
    """validate the reset token, uid and updates to new password."""
    password = serializers.CharField(write_only = True, min_length = 8)
    uidb64 = serializers.CharField(write_only = True)
    token = serializers.CharField(write_only= True)

    def validate(self, attrs):
        try:
            uid = force_str(urlsafe_base64_decode(attrs.get('uidb64')))
            user = CustomUser.objects.get(pk= uid)
        except(TypeError, ValueError, OverflowError,CustomUser.DoesNotExist):
            raise serializers.ValidationError({"error": "Invalid or expired reset link."})
        if not PasswordResetTokenGenerator().check_token(user,attrs.get('token')):
            raise serializers.ValidationError({"error":"Invalid or expired reset link."})
        
        attrs['user'] = user
        return attrs
    
class ChangePasswordSerializer(serializers.Serializer):
    """handles password updates for logged-in users requiring old password confirmation."""
    old_password = serializers.CharField(write_only=True, required= True)
    new_password = serializers.CharField(write_only = True, required= True, min_length =8)

    def validate_old_password(self, value):
        user = self.context['request'].user
        if not user.check_password(value):
            raise serializers.ValidationError("Your current password was intered incorrectly.")
        return value