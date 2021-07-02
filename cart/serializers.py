import re
from rest_framework import  serializers
from .models import OrderItem, Order
from glocery.serializers import GlocerySerializer
from recipe.serializers import RecipeSerializer


class OrderItemSerializer(serializers.ModelSerializer):
    recipe = RecipeSerializer(read_only=True)
    glocery = GlocerySerializer(read_only=True)
    class Meta:
        model=OrderItem
        fields="__all__"

class OrderSerializer(serializers.ModelSerializer):
    items = OrderItemSerializer(many=True, read_only=True)
    class Meta:
        model=Order
        fields="__all__"


class OrderItemSerializer(serializers.Serializer):
    type = serializers.CharField()
    recipe_id = serializers.IntegerField(required=False)
    glocery_id = serializers.IntegerField(required=False)
    email=serializers.EmailField()