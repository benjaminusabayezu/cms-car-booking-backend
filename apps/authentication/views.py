from django.shortcuts import render
from rest_framework import generics, status
from rest_framework.response import Response
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework_simplejwt.views import TokenObtainPairView
from .models import CustomUser
from .serializers import CustomTokenObtainPairSerializer,UserRegisterSerializer

# Create your views here.

class CustomTokenObtainPairView(TokenObtainPairView):
    """login view to  use cstomized  token payload"""
    serializer_class = CustomTokenObtainPairSerializer

class UserRegisterView(generics.CreateAPIView):
    """public endpoint for new clients to create accounts."""
    queryset = CustomUser.objects.all()
    serializer_class = UserRegisterSerializer
    permission_classes = [AllowAny]