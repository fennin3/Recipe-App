from django.urls import path
from . import views

urlpatterns = [
    path("get-all-categories/", views.GetAllCategories.as_view(), name="all_cat"),
    path("get-category-recipes/<id>/", views.GetCategoryRecipes.as_view(),name="cat_recipes"),
    path("get-all-recipes/", views.GetAllRecipes.as_view(), name="allrecipes"),
    path("get-featured-recipes/", views.GetFeaturedRecipes.as_view(), name="allfeaturedrecipes"),
    path("recipe-detail/<id>/", views.GetRecipeDetail.as_view(), name="recipe_detail"),
    path("save-recipe/", views.SaveRecipe.as_view(), name="save_recipe"),
    path("get-saved-recipes/<email>/", views.GetSavedRecipes.as_view(), name="get_sr"),
    path("remove-saved-recipe/<id>/", views.RemoveSavedRecipe.as_view(), name="remove_sr"),
    path("add-review/", views.AddReview.as_view(), name="add_review"),
    path("rate-recipe/", views.RateRecipe.as_view(), name="rate_recipe"),
    path("add-recipe-tip/", views.AddChefTips.as_view(), name="add_tip"),
    path("get-recommended-recipes/<email>/", views.GetRecommendedRecipes.as_view(), name="recommended"),
    path("get-scheduled-recipes/<email>/", views.GetscheduledRecipes.as_view(), name="sched_rec"),
    path("schedule-recipe/", views.CreateScheduledRecipe.as_view(), name="sch_r")

    
]
