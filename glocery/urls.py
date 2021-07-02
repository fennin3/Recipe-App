from django.urls import path
from . import views

urlpatterns = [
    path("get-all-categories/", views.GetAllCategories.as_view(), name="all_g_cat"),
    path("get-category-gloceries/<id>/", views.GetCategoryGloceries.as_view(),name="cat_g_recipes"),
    path("get-all-gloceries/", views.GetAllGloceries.as_view(), name="allglo"),
    path("glocery-detail/<id>/", views.GetGloceryDetail.as_view(), name="glo_detail"),
    path("save-glocery/", views.SaveGlocery.as_view(), name="save_glo"),
    path("get-saved-gloceries/<email>/", views.GetSavedGlocery.as_view(), name="get_g_sr"),
    path("remove-saved-glocery/<id>/", views.RemoveSavedGlocery.as_view(), name="remove_g_sr")
]
