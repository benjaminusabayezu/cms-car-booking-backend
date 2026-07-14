from django.urls import path,include
from rest_framework.routers import DefaultRouter
from .views import LandingPageConfigView, NavbarLinkViewSet

router = DefaultRouter()
router.register(r'navbar-links', NavbarLinkViewSet , basename ='navbar-link')

urlpatterns = [
    path('landing-page/', LandingPageConfigView.as_view(), name='landing-page-config'),
    path('',include(router.urls)),
]
