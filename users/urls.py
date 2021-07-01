from django.urls import path
from . import views

urlpatterns = [
    path('create-account/',views.CreateUserView.as_view(), name="create_account"),
    path("login/", views.UserLoginView.as_view(), name="login")
]
