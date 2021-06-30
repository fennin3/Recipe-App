from django.db import models
from recipe.models import Category, Review


class Category(models.Model):
    name = models.CharField(max_length=255)
    image = models.ImageField(upload_to="recipe_category/")



class Glocery(models.Model):
    name = models.CharField(max_length=255)
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name="recipes")
    image = models.ImageField(upload_to="recipe_images/")
    description = models.CharField(max_length=100000)
    price = models.DecimalField(default=0.00, decimal_places=2, max_digits=9)
    discount = models.DecimalField(default=0.00, decimal_places=2, max_digits=9)
    reviews = models.ManyToManyField(Review, null=True, blank=True)
 