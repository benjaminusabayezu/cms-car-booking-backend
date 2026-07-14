from django.db import models
from django.core.exceptions import ValidationError
# Create your models here.

class LandingPageConfig(models.Model):
    """model holding the core settings"""
    site_name = models.CharField(max_length=50, default= "CarX")
    hero_title = models.CharField(max_length=150, default="Find,Book and Rent a Car in Easy Steps")
    hero_subtitle = models.CharField(default="Get access to a diverse fleet of high-quality vehicles with flexible booking plans.")
    hero_cta_text =models.CharField(max_length=50, default="Explore Cars")
    hero_image = models.ImageField(upload_to='cms/hero/',blank=True, null=True)

    #footer element

    contact_email =models.CharField(default="support@carx.com")
    contact_phone = models.CharField(max_length=15, default="+250 784 445 193")
    updated_at =models.DateTimeField(auto_now=True)
    copyright_text =models.CharField(max_length=150, default=" 2026 CarX. All right reserved.")

    class Meta:
        verbose_name = "Landing page Configuration"
        verbose_name_plural ="Landing Page Configuration"
    
    def clean(self):
        """enforce singleton behavior"""
        if LandingPageConfig.objects.exists() and not self.pk:
            raise ValidationError("You can only create one Landing Page Configuration.")
        
    def save(self, *args , **kwargs):
        self.clean()
        super().save(*args, **kwargs)
    def __str__(self):
        return f"{self.site_name} - Landing Page Config"

class NavbarLink(models.Model):
    """dynamic navigation links"""
    label = models.CharField(max_length=50 , help_text="The display text for the link (e.g., 'Cars')")
    url_path = models.CharField(max_length=100, help_text="The react router route path (e.g., '/cars')")
    icon_name = models.CharField(max_length=50, blank=True, null=True,help_text="React icon class or string identifier (e.g., 'CarIcon')")
    order = models.PositiveIntegerField(default=0, help_text="Sorting order in the navbar")
    is_active=models.BooleanField(default=True)

    class Meta:
        ordering =['order']

    def __str__(self):
        return f"{self.label} ->{self.url_path}"
