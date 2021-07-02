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
    user = UserSerializer(read_only=True)
    class Meta:
        model=Tip
        fields="__all__"



class RatingSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)
    class Meta:
        model=Rating
        fields="__all__"


class RecipeSerializer(serializers.ModelSerializer):
    category = CategorySerializer(read_only=True)
    all_ratings = RatingSerializer(read_only=True, many=True)
    reviews = ReviewSerializer(many=True, read_only=True)
    tips_from_chef = TipSerializer(many=True,read_only=True)
    avg_rate = serializers.ReadOnlyField(source='average_rate')
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


class AddReviewSerializer(serializers.Serializer):
    email = serializers.EmailField()
    recipe_id = serializers.IntegerField()
    text = serializers.CharField()


class AddRateSerializer(serializers.Serializer):
    email = serializers.EmailField()
    recipe_id = serializers.IntegerField()
    rate = serializers.DecimalField(max_digits=3, decimal_places=2)

class AddTipSerializer(serializers.Serializer):
    email = serializers.EmailField()
    recipe_id = serializers.IntegerField()
    text = serializers.CharField()





