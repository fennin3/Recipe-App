from django.contrib import admin
from .models import *


admin.site.register(Review)
admin.site.register(Tip)
admin.site.register(Category)
admin.site.register(Recipe)
admin.site.register(SavedRecipe)
admin.site.register(Rating)