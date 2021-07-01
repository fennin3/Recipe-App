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