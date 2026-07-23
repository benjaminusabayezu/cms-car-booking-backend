from django.db import models,transaction
from django.db.models import F
from django.core.exceptions import ValidationError
# Create your models here.

class SingletonModel(models.Model):
    class Meta:
        abstract = True

    def clean(self):
        # Prevent creating multiple instances
        if self.__class__.objects.exists() and not self.pk:
            raise ValidationError(f"You can only create one {self._meta.verbose_name} record.")

    def save(self, *args, **kwargs):
        self.clean()
        super().save(*args, **kwargs)

class OrderedModel(models.Model):
    order = models.PositiveIntegerField(default=0)

    class Meta:
        abstract = True

    def save(self, *args, **kwargs):
        if self.order == 0:
            last_order = self.__class__.objects.aggregate(
                max_order=models.Max("order")
            )["max_order"]

            self.order = (last_order or 0) + 1

        super().save(*args, **kwargs)
class LandingPageConfig(SingletonModel):
    """model holding the core settings"""
    site_name = models.CharField(max_length=50, default= "CarX")
    hero_title = models.CharField(max_length=150, default="Find,Book and Rent a Car in Easy Steps")
    hero_subtitle = models.CharField(
    max_length=255,
    default="Get access to a diverse fleet of high-quality vehicles with flexible booking plans."
)
    hero_cta_text =models.CharField(max_length=50, default="Explore Cars")
    hero_image = models.ImageField(upload_to='cms/hero/',blank=True, null=True)

    #footer element

    contact_email = models.CharField(
    max_length=100,
    default="support@carx.com"
)
    contact_phone = models.CharField(max_length=25, default="0 784 445 193")
    updated_at =models.DateTimeField(auto_now=True)
    copyright_text =models.CharField(max_length=150, default=" 2026 CarX. All right reserved.")

    class Meta:
        verbose_name = "Landing page Hero Configuration"
        verbose_name_plural ="Landing Page Hero Configuration"
    
    def __str__(self):
        return f"{self.site_name} - Hero Page Config"

#Company Information (Singleton) ---
class CompanyInformation(SingletonModel):
    contact_email = models.EmailField(default="support@carx.com")
    contact_phone = models.CharField(max_length=20, default="+250 784 445 193")
    address = models.TextField(default="Kigali, Rwanda", blank=True)
    about_us_short = models.TextField(help_text="A brief snippet about your company", blank=True)
    
    class Meta:
        verbose_name = "Company Information"
        verbose_name_plural = "Company Information"

    def __str__(self):
        return "Company Information Settings"

#Footer Configuration (Singleton) ---
class FooterConfig(SingletonModel):
    copyright_text = models.CharField(max_length=150, default="© 2026 CarX. All rights reserved.")
    footer_bottom_text = models.CharField(max_length=250, blank=True, help_text="Any additional small print or links.")

    class Meta:
        verbose_name = "Footer Configuration"
        verbose_name_plural = "Footer Configuration"

    def __str__(self):
        return "Footer Configuration Settings"
class Service(OrderedModel):
    title = models.CharField(max_length=100)
    description = models.TextField()
    icon_name = models.CharField(
        max_length=50, 
        help_text="CSS class or Lucide/FontAwesome icon name (e.g., 'car', 'calendar')", 
        blank=True
    )

    class Meta:
        ordering = ['order']

    def __str__(self):
        return self.title



class Feature(OrderedModel):
    title = models.CharField(max_length=100)
    description = models.TextField()
    image = models.ImageField(upload_to='cms/features/', blank=True, null=True)
    
    class Meta:
        ordering = ['order']

    def save(self, *args, **kwargs):
        if self.order == 0:
            last_order = Feature.objects.aggregate(
                max_order=models.Max("order")
            )["max_order"]

            self.order = (last_order or 0) + 1

        super().save(*args, **kwargs)

    def __str__(self):
        return self.title

class FAQ(OrderedModel):
    question = models.CharField(max_length=255)
    answer = models.TextField()
    
    class Meta:
        verbose_name = "FAQ"
        verbose_name_plural = "FAQs"
        ordering = ['order']

    def __str__(self):
        return self.question
    
class Testimonial(OrderedModel):
    client_name = models.CharField(max_length=100)
    client_role = models.CharField(max_length=100, help_text="e.g. CEO, Customer, Traveler", blank=True)
    client_avatar = models.ImageField(upload_to='cms/testimonials/', blank=True, null=True)
    review_text = models.TextField()
    rating = models.PositiveIntegerField(default=5, help_text="Star rating from 1 to 5")

    class Meta:
        ordering =['order']
    def __str__(self):
        return f"Testimonial from {self.client_name}"

class SocialLink(OrderedModel):
    PLATFORM_CHOICES = [
        ('facebook', 'Facebook'),
        ('twitter', 'Twitter / X'),
        ('instagram', 'Instagram'),
        ('linkedin', 'LinkedIn'),
        ('youtube', 'YouTube'),
    ]
    platform = models.CharField(max_length=50, choices=PLATFORM_CHOICES)
    url = models.URLField()
    is_active = models.BooleanField(default=True)

    class Meta:
        ordering =['order']

    def __str__(self):
        return f"{self.get_platform_display()} Link"
class NavbarLink(OrderedModel):
    """dynamic navigation links"""
    label = models.CharField(max_length=50 , help_text="The display text for the link (e.g., 'Cars')")
    url_path = models.CharField(max_length=100, help_text="The react router route path (e.g., '/cars')")
    icon_name = models.CharField(max_length=50, blank=True, null=True,help_text="React icon class or string identifier (e.g., 'CarIcon')")
    is_active=models.BooleanField(default=True)

    class Meta:
        ordering =['order']

    def __str__(self):
        return f"{self.label} ->{self.url_path}"
