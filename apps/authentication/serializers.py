from rest_framework import serializers
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
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

    def create(self, validate_data):
        #client Register publlically
        user = CustomUser.objects.create_user(
            username= validate_data['username'],
            email= validate_data['email'],
            password=validate_data['password'],
            phone_number = validate_data.get('phone_number', ''),
            role = 'CLIENT'
        )
        return user