from django.db import models
from django.contrib.auth.models import AbstractUser


# Create your models here.

class CustomUser(AbstractUser):
    ROLE_CHOICES =(
        ('ADMIN','Admin'),
        ('MANAGER','Manager'),
        ('CLIENT', 'Client'),
    )
 
    email = models.EmailField(unique=True)
    role = models.CharField(max_length=50, choices= ROLE_CHOICES, default='CLIENT')
    phone_number = models.CharField(max_length=15, blank=True,null=True)

    #let me use email as primary for login identifier
    USERNAME_FIELD ='email'
    REQUIRED_FIELDS=['username']

    def __str__(self):
        return f"{self.email} {self.role}"