from django.db import models
from django.db.models import Sum
from django.db.models.base import Model



class Review(models.Model):
    user = models.ForeignKey("users.CustomUser", on_delete=models.CASCADE, related_name="reviews")
    text = models.CharField(max_length=20000)
    date_posted = models.DateTimeField(auto_now_add=True)




class Tip(models.Model):
    user = models.ForeignKey("users.CustomUser", on_delete=models.CASCADE, related_name="tips")
    text = models.CharField(max_length=20000)
    date_posted = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Tip from {self.user.full_name}"
    

class TipImage(models.Model):
    image=models.ImageField(upload_to="images/tip_images/")
    tip = models.ForeignKey(Tip, on_delete=models.CASCADE, related_name="images")


class Ingredient(models.Model):
    description = models.CharField(max_length=100000)

class IngredientItem(models.Model):
    text = models.CharField(max_length=100000)
    image = models.ImageField(upload_to='images/ingredient_images/')
    ingredient = models.ForeignKey(Ingredient, on_delete=models.CASCADE, related_name='items')

class Category(models.Model):
    name = models.CharField(max_length=255)
    image = models.ImageField(upload_to="images/recipe_category/")

    def __str__(self):
        return self.name

class Rating(models.Model):
    user = models.ForeignKey("users.CustomUser", on_delete=models.CASCADE)
    rate = models.FloatField(default=0.0)
    date = models.DateTimeField(auto_now=True)

class Event(models.Model):
    name = models.CharField(max_length=100)
    image=models.ImageField(upload_to="images/event_images/", null=True, blank=True)

    def __str__(self):
        return self.name
    

class Recipe(models.Model):
    name = models.CharField(max_length=255)
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name="recipes")
    image = models.ImageField(upload_to="images/recipe_images/", blank=True, null=True)
    no_of_consumers = models.IntegerField(default=1)
    # nutritional_details = models.CharField(max_length=100000, null=True, blank=True)
    cuisine = models.CharField(max_length=200)
    calories = models.CharField(max_length=200)
    min_duration = models.IntegerField()
    max_duration = models.IntegerField()
    attribution = models.CharField(max_length=30, null=True, blank=True)
    description = models.CharField(max_length=100000)
    ingredient = models.ForeignKey(Ingredient, on_delete=models.CASCADE, related_name="ingre_recipes")
    allergies = models.JSONField(default={'title':'','description':''},)
    price = models.DecimalField(default=0.00, decimal_places=2, max_digits=9)
    discount = models.DecimalField(default=0.00, decimal_places=2, max_digits=9)
    all_ratings = models.ManyToManyField(Rating, null=True, blank=True)
    raters = models.ManyToManyField("users.CustomUser", null=True, blank=True, related_name="rated_recipes")
    raters_ids = models.ManyToManyField("users.CustomUser", null=True, blank=True, related_name="r")
    rating = models.DecimalField(default=0.0, decimal_places=1, max_digits=1)
    reviews = models.ManyToManyField(Review, null=True, blank=True)
    tips_from_chef = models.ManyToManyField(Tip, null=True, blank=True)
    vid_instruction = models.FileField(upload_to="videos/video_instructions/", blank=True, null=True)
    text_instruction = models.CharField(max_length=100000, null=True, blank=True)
    event = models.ForeignKey(Event, on_delete=models.CASCADE, related_name="event_recipes", null=True,blank=True)
    date_posted = models.DateTimeField(auto_now_add=True, null=True, blank=True)
    featured = models.BooleanField(default=False)

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


class NutritionalFact(models.Model):
    text = models.CharField(max_length=500)
    value = models.CharField(max_length=200)
    recipe = models.ForeignKey(Recipe, on_delete=models.CASCADE, related_name="nutri_details", null=True, blank=True)

class SavedRecipe(models.Model):
    user = models.ForeignKey("users.CustomUser", on_delete=models.CASCADE, related_name="saved_recipes")
    recipe = models.ForeignKey(Recipe, on_delete=models.CASCADE, related_name="recipe_saves")
    date_saved = models.DateTimeField(auto_now_add=True)

class ScheduledRecipe(models.Model):
    recipe = models.ForeignKey(Recipe, on_delete=models.CASCADE, related_name="sche_recipes")
    user = models.ForeignKey("users.CustomUser", on_delete=models.CASCADE, related_name="sche_recipes_fu")
    date_to_order = models.CharField(max_length=20)
    date = models.DateTimeField(auto_now_add=True)



    