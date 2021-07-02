from django.urls import path
from . import views


urlpatterns = [
    path("get-all-categories/", views.GetCategories.as_view(), name="all_c_cat"),
    path("get-category-posts/<id>/", views.GetPostsOfACategory.as_view(), name="posts_of_cat"),
    path("get-all-posts/", views.GetAllPosts.as_view(), name="all_posts"),
    path("get-post-detail/<id>/", views.GetPostDetail.as_view(), name="post_detail"),
    path("comment-on-post/", views.CommentOnPost.as_view(), name="post_comment")
]
