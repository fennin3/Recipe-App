from rest_framework import serializers
from recipe.models import *



class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model=Category
        fields="__all__"


class ReviewSerializer(serializers.ModelSerializer):
    class Meta:
        model=Review
        fields="__all__"


class TipSerializer(serializers.ModelSerializer):
    class Meta:
        model=Tip
        fields="__all__"


class RecipeSerializer(serializers.ModelSerializer):
    category = CategorySerializer(read_only=True)
    # raters = 
    reviews = ReviewSerializer(many=True, read_only=True)
    tips_from_chef = TipSerializer(many=True,read_only=True)
    class Meta:
        model=Recipe
        fields="__all__"
