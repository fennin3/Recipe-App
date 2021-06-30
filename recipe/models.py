from django.db import models
from django.contrib.auth import get_user_model


User = get_user_model()


class Review(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="reviews")
    text = models.CharField(max_length=20000)
    date_posted = models.DateTimeField(auto_now_add=True)

class Tip(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="tips")
    text = models.CharField(max_length=20000)
    date_posted = models.DateTimeField(auto_now_add=True)

class Category(models.Model):
    name = models.CharField(max_length=255)
    image = models.ImageField(upload_to="recipe_category/")

class Recipe(models.Model):
    name = models.CharField(max_length=255)
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name="recipes")
    image = models.ImageField(upload_to="recipe_images/")
    no_of_consumers = models.IntegerField(default=1)
    nutritional_details = models.CharField(max_length=100000)
    min_duration = models.IntegerField()
    max_duration = models.IntegerField()
    attribution = models.CharField(max_length=30)
    description = models.CharField(max_length=100000)
    ingredient = models.CharField(max_length=100000)
    allergies = models.CharField(max_length=100000)
    price = models.DecimalField(default=0.00, decimal_places=2, max_digits=9)
    discount = models.DecimalField(default=0.00, decimal_places=2, max_digits=9)
    total_rating = models.DecimalField(default=0.0, decimal_places=2, max_digits=2)
    raters = models.ManyToManyField(User, null=True, blank=True)
    rating = models.DecimalField(default=0.0, decimal_places=2, max_digits=2)
    reviews = models.ManyToManyField(Review, null=True, blank=True)
    tips_from_chef = models.ManyToManyField(Tip, null=True, blank=True)
    vid_instruction = models.FileField(upload_to="video_instructions/")
    text_instruction = models.CharField(max_length=100000)
    