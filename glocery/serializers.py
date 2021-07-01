from rest_framework import serializers
from .models import *
from recipe.serializers import ReviewSerializer


class CategorySerializer(serializers.ModelSerializer):
    model=Category
    fields="__all__"


class GlocerySerializer(serializers.ModelSerializer):
    category = CategorySerializer(read_only=True)
    reviews = ReviewSerializer(many=True, read_only=True)
    model=Glocery
    fields="__all__"
