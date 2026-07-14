from django.shortcuts import render
from rest_framework import status, views, viewsets
from rest_framework.response import Response
from rest_framework.permissions import AllowAny
from apps.authentication.permissions import IsAdminUserRole
from .models import LandingPageConfig, NavbarLink
from .serializers import LandingPageConfigSerializer,NavbarLinkSerializer

# Create your views here.

class LandingPageConfigView(views.APIView):
    """API to retrieve(public) or update(admin Only) the global Landing."""
    def get_permissions(self):
        if self.request.method == 'GET':
            return [AllowAny()]
        return [IsAdminUserRole()]
    def get(self, request):
        config, created = LandingPageConfig.objects.get_or_create(id=1)
        serializer = LandingPageConfigSerializer(config, context={'request': request})
        return Response(serializer.data)
    
    def put(self, request):
        config, created = LandingPageConfig.objects.get_or_create(id=1)
        serializer = LandingPageConfigSerializer(config, data=request.data, partial=True,context={'request':request})

        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status = status.HTTP_400_BAD_REQUEST)
    
class NavbarLinkViewSet(viewsets.ModelViewSet):
    "CRUD endpoint for navbar link control"
    queryset = NavbarLink.objects.all()
    serializer_class = NavbarLinkSerializer

    def get_permissions(self):
        if self.action in ['list', 'retrieve']:
            return [AllowAny()]
        return [IsAdminUserRole()]