from django.db import models
from recipe.models import Recipe
from glocery.models import Glocery
from django.contrib.auth import get_user_model


User = get_user_model()

class OrderItem(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)
    type = models.CharField(max_length=20)
    recipe = models.ForeignKey(Recipe, on_delete=models.CASCADE, null=True, blank=True)
    glocery = models.ForeignKey(Glocery, on_delete=models.CASCADE, null=True, blank=True)
    quantity = models.IntegerField(default=1)
    date_added = models.DateTimeField(auto_now_add=True)
    date_updated = models.DateTimeField(auto_now=True)


class Order(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="order")
    items = models.ManyToManyField(OrderItem, null=True, blank=True)
    ordered = models.BooleanField(default=False)
    date_added = models.DateTimeField(auto_now_add=True)
    date_updated = models.DateTimeField(auto_now=True)
