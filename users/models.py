from django.db import models
from django.contrib.auth.models import AbstractUser
from django.contrib.auth import get_user_model




User = get_user_model()


class CustomUser(AbstractUser):
    username = None
    email = models.EmailField(unique=True)
    USERNAME_FIELD = 'email'
    full_name = models.CharField(max_length=255)
    profile_pic = models.ImageField(upload_to="Profile_pic/")
    phone = models.CharField(max_length=16)
    REQUIRED_FIELDS = []


class Address(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="addresses")
    name = models.CharField(max_length=500)
    recipient_name = models.CharField(max_length=500)
    recipient_phone = models.CharField(max_length=16)
    address = models.CharField(max_length=1000)
    town = models.CharField(max_length=500)
    city = models.CharField(max_length=500)
    instruction = models.CharField(max_length=10000)
