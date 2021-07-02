from glocery.models import Glocery, SavedGlocery, GloceryCategory
from django.contrib import admin


admin.site.register(GloceryCategory)
admin.site.register(Glocery)
admin.site.register(SavedGlocery)