from django.db import models
from recipe.models import Review
from django.contrib.auth import get_user_model

User = get_user_model()


class GloceryCategory(models.Model):
    name = models.CharField(max_length=255)
    image = models.ImageField(upload_to="glocery_category/")



class Glocery(models.Model):
    name = models.CharField(max_length=255)
    category = models.ForeignKey(GloceryCategory, on_delete=models.CASCADE, related_name="gloceries")
    image = models.ImageField(upload_to="recipe_images/")
    description = models.CharField(max_length=100000)
    price = models.DecimalField(default=0.00, decimal_places=2, max_digits=9)
    discount = models.DecimalField(default=0.00, decimal_places=2, max_digits=9)
    reviews = models.ManyToManyField(Review, null=True, blank=True)


class SavedGlocery(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="saved_gloceries")
    glocery = models.ForeignKey(Glocery, on_delete=models.CASCADE, related_name="glocery_saves")
    date_saved = models.DateTimeField(auto_now_add=True)
    
 