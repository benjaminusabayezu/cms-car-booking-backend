from rest_framework import  serializers
from .models import (LandingPageConfig,
                      NavbarLink,
                      CompanyInformation,
                      FooterConfig,
                      Feature, FAQ, Service, Testimonial, SocialLink
                      )

class LandingPageConfigSerializer(serializers.ModelSerializer):
    class Meta:
        model = LandingPageConfig
        fields = '__all__'
        extra_kwargs = {
            'hero_image': {'required': False, 'allow_null': True},
        }
class CompanyInformationSerializer(serializers.ModelSerializer):
    class Meta:
        model = CompanyInformation
        fields = '__all__'

class FooterConfigSerializer(serializers.ModelSerializer):
    class Meta:
        model = FooterConfig
        fields = '__all__'
class ServiceSerializer(serializers.ModelSerializer):
    class Meta:
        model = Service
        fields = '__all__'

class FeatureSerializer(serializers.ModelSerializer):
    class Meta:
        model = Feature
        fields = '__all__'
        extra_kwargs = {
            'image': {'required': False, 'allow_null': True},
        }

class FAQSerializer(serializers.ModelSerializer):
    class Meta:
        model = FAQ
        fields = '__all__'


# --- 7. Testimonial Serializer ---
class TestimonialSerializer(serializers.ModelSerializer):
    class Meta:
        model = Testimonial
        fields = '__all__'
        extra_kwargs = {
            'client_avatar': {'required': False, 'allow_null': True},
        }


# --- 8. Social Link Serializer ---
class SocialLinkSerializer(serializers.ModelSerializer):
    platform_display = serializers.CharField(source='get_platform_display', read_only=True)

    class Meta:
        model = SocialLink
        fields = ['id', 'platform', 'platform_display', 'url', 'is_active']
class NavbarLinkSerializer(serializers.ModelSerializer):
    class Meta:
        model = NavbarLink
        fields =['id','label','url_path','icon_name','order','is_active']