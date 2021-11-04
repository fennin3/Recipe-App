from rest_framework import serializers, status
from rest_framework.response import Response
from rest_framework.views import APIView
from recipe.models import *
from django.contrib.auth import get_user_model


User = get_user_model()

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

class TipImageSerializer(serializers.ModelSerializer):
    class Meta:
        model=TipImage
        fields=['id','image']


class TipSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)
    images=TipImageSerializer(read_only=True, many=True)
    class Meta:
        model=Tip
        fields="__all__"


class IngredientItemSerializer(serializers.ModelSerializer):
    class Meta:
        model=IngredientItem
        fields=['text', 'image']


class IngredientSerializer(serializers.ModelSerializer):
    items = IngredientItemSerializer(read_only=True, many=True)
    class Meta:
        model=Ingredient
        fields="__all__"

class RatingSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)
    class Meta:
        model=Rating
        fields="__all__"

class NutriDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model=NutritionalFact
        fields=['text','value']

class EventSerializer(serializers.ModelSerializer):
    class Meta:
        model=Event
        fields='__all__'


class RecipeSerializer(serializers.ModelSerializer):
    category = CategorySerializer(read_only=True)
    all_ratings = RatingSerializer(read_only=True, many=True)
    reviews = ReviewSerializer(many=True, read_only=True)
    tips_from_chef = TipSerializer(many=True,read_only=True)
    ingredient = IngredientSerializer(read_only=True)
    avg_rate = serializers.ReadOnlyField(source='average_rate')
    nutri_details = NutriDetailSerializer(read_only=True, many=True)
    event = EventSerializer(read_only=True)

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
    rate = serializers.DecimalField(max_digits=3, decimal_places=2)

class AddTipSerializer(serializers.Serializer):
    email = serializers.EmailField()
    recipe_id = serializers.IntegerField()
    text = serializers.CharField()

class ScheduleRecipeSerializer(serializers.Serializer):
    recipe_id = serializers.IntegerField()
    user_email = serializers.EmailField()
    date=serializers.CharField()

class ListSchedRecipesSerializer(serializers.ModelSerializer):
    recipe = RecipeSerializer(read_only=True)
    class Meta:
        model=ScheduledRecipe
        fields="__all__"

class ListEventSerializer(serializers.ModelSerializer):
    event_recipes= RecipeSerializer(read_only=True, many=True)
    class Meta:
        model=Event
        fields='__all__'



