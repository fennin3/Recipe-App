from django.db import models
from django.contrib.auth import get_user_model
from django.db.models import Sum


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

    def __str__(self):
        return self.name

class Rating(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    rate = models.FloatField(default=0.0)
    date = models.DateTimeField(auto_now=True)

class Recipe(models.Model):
    name = models.CharField(max_length=255)
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name="recipes")
    image = models.ImageField(upload_to="recipe_images/", blank=True, null=True)
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
    all_ratings = models.ManyToManyField(Rating, null=True, blank=True)
    raters = models.ManyToManyField(User, null=True, blank=True, related_name="rated_recipes")
    raters_ids = models.ManyToManyField(User, null=True, blank=True, related_name="r")
    rating = models.DecimalField(default=0.0, decimal_places=1, max_digits=1)
    reviews = models.ManyToManyField(Review, null=True, blank=True)
    tips_from_chef = models.ManyToManyField(Tip, null=True, blank=True)
    vid_instruction = models.FileField(upload_to="video_instructions/", blank=True, null=True)
    text_instruction = models.CharField(max_length=100000, null=True, blank=True)
    date_posted = models.DateTimeField(auto_now_add=True, null=True, blank=True)

    @property
    def average_rate(self):
        total_rate = self.all_ratings.aggregate(Sum('rate'))

        total = total_rate['rate__sum']

        if total == None:
            return 0.0
        else:
        
            avg = total / len(self.raters.all())
            avg = round(avg,1)
            return avg

    def __str__(self):
        return self.name


class SavedRecipe(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="saved_recipes")
    recipe = models.ForeignKey(Recipe, on_delete=models.CASCADE, related_name="recipe_saves")
    date_saved = models.DateTimeField(auto_now_add=True)
    
    