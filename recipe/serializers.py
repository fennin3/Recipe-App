from rest_framework import serializers, status
from rest_framework.response import Response
from rest_framework.views import APIView
from recipe.models import *





class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model=User
        fields=['id','email','full_name','profile_pic','phone','language','points','notifications','email_news','special_offers', 'more_info']

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
    raters = UserSerializer(read_only=True, many=True)
    reviews = ReviewSerializer(many=True, read_only=True)
    tips_from_chef = TipSerializer(many=True,read_only=True)
    class Meta:
        model=Recipe
        fields="__all__"


class SaveRecipeSerializer(serializers.Serializer):
    email = serializers.EmailField()
    id = serializers.IntegerField()


class SavedRecipeSerializer(serializers.ModelSerializer):
    # user = UserSerializer(read_only=True)
    recipe = RecipeSerializer(read_only=True)
    class Meta:
        model=SavedRecipe
        fields="__all__"


