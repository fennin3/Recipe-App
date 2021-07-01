from django.db import models
from django.contrib.auth.models import AbstractUser


# User = get_user_model()

# addresses
# payments_methods
# more_info 
# referrals

class CustomUser(AbstractUser):
    username = None
    email = models.EmailField(unique=True)
    USERNAME_FIELD = 'email'
    full_name = models.CharField(max_length=255)
    profile_pic = models.ImageField(upload_to="Profile_pic/", null=True, blank=True)
    phone = models.CharField(max_length=16)
    language = models.CharField(max_length=10, default="en")
    points = models.IntegerField(default=0)
    notifications = models.BooleanField(default=False)  # in app notifications
    email_news = models.BooleanField(default=False) # email and news letter
    special_offers = models.BooleanField(default=True)
    email_verified = models.BooleanField(default=False)
    REQUIRED_FIELDS = []


class Address(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name="addresses")
    name = models.CharField(max_length=500)
    recipient_name = models.CharField(max_length=500)
    recipient_phone = models.CharField(max_length=16)
    address = models.CharField(max_length=1000)
    town = models.CharField(max_length=500)
    city = models.CharField(max_length=500)
    instruction = models.CharField(max_length=10000)
    date_added = models.DateTimeField(auto_now_add=True)

class PaymentMethods(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name="payments_methods")
    type = models.CharField(max_length=10)
    momo_name = models.CharField(max_length=255, null=True, blank=True)
    momo_number = models.CharField(max_length=16, null=True, blank=True)
    holder_name = models.CharField(max_length=255, null=True, blank=True)
    card_number = models.CharField(max_length=16, null=True, blank=True)
    exp_month = models.IntegerField(null=True, blank=True)
    exp_year = models.IntegerField(null=True, blank=True)
    date_added = models.DateTimeField(auto_now_add=True)

 


class AdditionalInfo(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name="more_info")
    referred_by = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name="referrals")

from recipe.models import Recipe
from glocery.models import Glocery


class PreOrderingCalender(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name="calender", null=True, blank=True)
    item_type = models.CharField(max_length=50, null=True)
    # item_id = models.IntegerField()
    recipe = models.ForeignKey(Recipe, on_delete=models.CASCADE, null=True, blank=True)
    glocery = models.ForeignKey(Glocery, on_delete=models.CASCADE, null=True, blank=True)
    date_to_order = models.DateField(auto_now_add=True)



class OTPCode(models.Model):
    code = models.CharField(max_length=7)
    email = models.EmailField()