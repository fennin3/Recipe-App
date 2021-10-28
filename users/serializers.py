from users.models import *
from rest_framework import serializers
from django.contrib.auth import get_user_model, authenticate
from recipe.serializers import RecipeSerializer
from glocery.serializers import GlocerySerializer
from rest_framework_jwt.settings import api_settings
from django.contrib.auth.models import update_last_login


User = get_user_model()
JWT_PAYLOAD_HANDLER = api_settings.JWT_PAYLOAD_HANDLER
JWT_ENCODE_HANDLER = api_settings.JWT_ENCODE_HANDLER

class AdditionalInfoSerializer(serializers.ModelSerializer):
    class Meta:
        model=AdditionalInfo
        fields="__all__"

class AddressSerializer(serializers.ModelSerializer):
    class Meta:
        model=Address
        fields="__all__"

class UserSerializer(serializers.ModelSerializer):
    addresses = AddressSerializer(read_only=True, many=True)
    class Meta:
        model=User
        fields=['id','email','full_name','profile_pic','phone','language','points','notifications','email_news','special_offers', 'addresses']




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


class CreateUserSerializer(serializers.ModelSerializer):
    class Meta:
        model=User
        fields=['email','full_name','profile_pic','phone','notifications','email_news','special_offers', 'password']


class UserLoginSerializer(serializers.Serializer):
    email = serializers.EmailField()
    password = serializers.CharField()


class LanguageSerializer(serializers.ModelSerializer):
    class Meta:
        model=Language
        fields="__all__"


    # def validate(self, data):
    #     email_or_contact = data.get("email", None)
    #     password = data.get("password", None)

        

    #     user = authenticate(email=email_or_contact, password=password)
        

    #     if user is None:
    #         raise serializers.ValidationError(
    #             'A user with this email/phone and password is not found.'
    #         )
    #     try:
    #         payload = JWT_PAYLOAD_HANDLER(user)
    #         jwt_token = JWT_ENCODE_HANDLER(payload)
    #         update_last_login(None, user)
    #     except User.DoesNotExist:
    #         raise serializers.ValidationError(
    #             'User with given email and password does not exists'
    #         )
    #     return {
    #         'email':email_or_contact,
    #         'username':user.username,
    #         'token': jwt_token
    #     }

