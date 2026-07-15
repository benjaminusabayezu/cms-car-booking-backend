from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import (
    PublicLandingPageDataView,
    LandingPageConfigView,
    CompanyInformationView,
    FooterConfigView,
    NavbarLinkViewSet,
    ServiceViewSet,
    FeatureViewSet,
    FAQViewSet,
    TestimonialViewSet,
    SocialLinkViewSet
)

router = DefaultRouter()
router.register(r'navbar-links', NavbarLinkViewSet, basename='navbarlink')
router.register(r'services', ServiceViewSet, basename='service')
router.register(r'features', FeatureViewSet, basename='feature')
router.register(r'faqs', FAQViewSet, basename='faq')
router.register(r'testimonials', TestimonialViewSet, basename='testimonial')
router.register(r'social-links', SocialLinkViewSet, basename='sociallink')

urlpatterns = [
    # Consolidated fast landing page payload
    path('landing-page/all/', PublicLandingPageDataView.as_view(), name='landing-page-all'),
    
    # Singleton updates
    path('landing-page/config/', LandingPageConfigView.as_view(), name='landing-page-config'),
    path('landing-page/company-info/', CompanyInformationView.as_view(), name='company-info'),
    path('landing-page/footer/', FooterConfigView.as_view(), name='footer-config'),
    
    # Rest of the collection CRUD endpoints (services, faqs, etc.)
    path('', include(router.urls)),
]