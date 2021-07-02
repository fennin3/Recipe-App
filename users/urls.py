from django.urls import path
from . import views

urlpatterns = [
    path('create-account/',views.CreateUserView.as_view(), name="create_account"),
    path("login/", views.UserLoginView.as_view(), name="login"),
    path('verify-email/', views.VerifyEmailView.as_view(),name="verify_email"),
    path("set-notifications/", views.SetNotitfications.as_view(), name="noti"),
    path("set-language/", views.SetLanguage.as_view(), name="lange"),
    path("retrieve-languages/", views.RetrieveAllLanguages.as_view(), name="all_lang")
]
