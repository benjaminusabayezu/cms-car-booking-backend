from django.shortcuts import render
from rest_framework import status, views, viewsets
from rest_framework.response import Response
from rest_framework.permissions import AllowAny
from apps.authentication.permissions import IsAdminUserRole

from .models import (
    LandingPageConfig, 
    NavbarLink, 
    CompanyInformation, 
    FooterConfig, 
    Service, 
    Feature, 
    FAQ, 
    Testimonial, 
    SocialLink
)
from .serializers import (
    LandingPageConfigSerializer, 
    NavbarLinkSerializer,
    CompanyInformationSerializer,
    FooterConfigSerializer,
    ServiceSerializer,
    FeatureSerializer,
    FAQSerializer,
    TestimonialSerializer,
    SocialLinkSerializer
)

# --- 1. Admin-Protected Custom Permission Helper ---
class AdminOrReadOnlyPermissionMixin:
    """Helper mixin to set GET requests to public, and modifying requests to Admin-Only."""
    def get_permissions(self):
        if self.request.method in ['GET', 'HEAD', 'OPTIONS']:
            return [AllowAny()]
        return [IsAdminUserRole()]


# --- 2. Unified Landing Page Payload (Highly Recommended for Frontend) ---
class PublicLandingPageDataView(views.APIView):
    """
    Public API endpoint to pull the entire landing page state (including 
    all singletons and list collections) in a single network request.
    """
    permission_classes = [AllowAny]

    def get(self, request):
        config, _ = LandingPageConfig.objects.get_or_create(id=1)
        company, _ = CompanyInformation.objects.get_or_create(id=1)
        footer, _ = FooterConfig.objects.get_or_create(id=1)
        
        context = {'request': request}

        return Response({
            "config": LandingPageConfigSerializer(config, context=context).data,
            "company": CompanyInformationSerializer(company, context=context).data,
            "footer": FooterConfigSerializer(footer, context=context).data,
            "navbar_links": NavbarLinkSerializer(NavbarLink.objects.all(), many=True, context=context).data,
            "services": ServiceSerializer(Service.objects.all(), many=True, context=context).data,
            "features": FeatureSerializer(Feature.objects.all(), many=True, context=context).data,
            "faqs": FAQSerializer(FAQ.objects.all(), many=True, context=context).data,
            "testimonials": TestimonialSerializer(Testimonial.objects.all(), many=True, context=context).data,
            "social_links": SocialLinkSerializer(SocialLink.objects.filter(is_active=True), many=True, context=context).data,
        })


# --- 3. Base Singleton Configuration View ---
class BaseSingletonView(AdminOrReadOnlyPermissionMixin, views.APIView):
    """Base APIView logic for singleton configuration models."""
    model = None
    serializer_class = None

    def get_object(self):
        obj, _ = self.model.objects.get_or_create(id=1)
        return obj

    def get(self, request):
        obj = self.get_object()
        serializer = self.serializer_class(obj, context={'request': request})
        return Response(serializer.data)

    def put(self, request):
        obj = self.get_object()
        serializer = self.serializer_class(obj, data=request.data, partial=True, context={'request': request})
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


# --- 4. Concrete Singleton Views ---

class LandingPageConfigView(BaseSingletonView):
    """API to retrieve (public) or update (admin-only) global Hero & Branding configs."""
    model = LandingPageConfig
    serializer_class = LandingPageConfigSerializer


class CompanyInformationView(BaseSingletonView):
    """API to retrieve (public) or update (admin-only) Company Contact & About details."""
    model = CompanyInformation
    serializer_class = CompanyInformationSerializer


class FooterConfigView(BaseSingletonView):
    """API to retrieve (public) or update (admin-only) Footer settings."""
    model = FooterConfig
    serializer_class = FooterConfigSerializer


# --- 5. Multi-item Model ViewSets ---

class NavbarLinkViewSet(AdminOrReadOnlyPermissionMixin, viewsets.ModelViewSet):
    queryset = NavbarLink.objects.all()
    serializer_class = NavbarLinkSerializer


class ServiceViewSet(AdminOrReadOnlyPermissionMixin, viewsets.ModelViewSet):
    queryset = Service.objects.all()
    serializer_class = ServiceSerializer


class FeatureViewSet(AdminOrReadOnlyPermissionMixin, viewsets.ModelViewSet):
    queryset = Feature.objects.all()
    serializer_class = FeatureSerializer


class FAQViewSet(AdminOrReadOnlyPermissionMixin, viewsets.ModelViewSet):
    queryset = FAQ.objects.all()
    serializer_class = FAQSerializer


class TestimonialViewSet(AdminOrReadOnlyPermissionMixin, viewsets.ModelViewSet):
    queryset = Testimonial.objects.all()
    serializer_class = TestimonialSerializer


class SocialLinkViewSet(AdminOrReadOnlyPermissionMixin, viewsets.ModelViewSet):
    queryset = SocialLink.objects.all()
    serializer_class = SocialLinkSerializer