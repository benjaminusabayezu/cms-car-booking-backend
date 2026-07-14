from rest_framework import  serializers
from .models import LandingPageConfig, NavbarLink

class LandingPageConfigSerializer(serializers.ModelSerializer):
    class Meta:
        model = LandingPageConfig
        fields = '__all__'
        extra_kwargs = {
            'logo': {'required': False, 'allow_null': True},
            'hero_image': {'required': False, 'allow_null': True},
        }

class NavbarLinkSerializer(serializers.ModelSerializer):
    class Meta:
        model = NavbarLink
        fields =['id','label','url_path','icon_name','order','is_active']