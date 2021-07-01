from users.models import *
from rest_framework import serializers
from django.contrib.auth import get_user_model
from recipe.serializers import RecipeSerializer
from glocery.serializers import GlocerySerializer

User = get_user_model()

class AdditionalInfoSerializer(serializers.ModelSerializer):
    class Meta:
        model=AdditionalInfo
        fields="__all__"

class UserSerializer(serializers.ModelSerializer):
    more_info = AdditionalInfoSerializer(read_only=True)
    class Meta:
        model=User
        fields=['id','email','full_name','profile_pic','phone','language','points','notifications','email_news','special_offers', 'more_info']


class AddressSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)
    class Meta:
        model=Address
        fields="__all__"

class PaymentSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)
    class Meta:
        model=PaymentMethods
        fields="__all__"


class PreOrderingCalenderSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)
    recipe= RecipeSerializer(read_only=True)
    glocery = GlocerySerializer(read_only=True)
    class Meta:
        model=PreOrderingCalender
        fields="__all__"
