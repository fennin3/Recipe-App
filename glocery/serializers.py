from rest_framework import serializers
from .models import *
from recipe.serializers import ReviewSerializer


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model=GloceryCategory
        fields="__all__"


class GlocerySerializer(serializers.ModelSerializer):
    category = CategorySerializer(read_only=True)
    reviews = ReviewSerializer(many=True, read_only=True)
    class Meta:
        model=Glocery
        fields="__all__"



class SaveGlocerySerializer(serializers.Serializer):
    email = serializers.EmailField()
    id = serializers.IntegerField()


class SavedGlocerySerializer(serializers.ModelSerializer):
    # user = UserSerializer(read_only=True)
    glocery = GlocerySerializer(read_only=True)
    class Meta:
        model=SavedGlocery
        fields="__all__"
