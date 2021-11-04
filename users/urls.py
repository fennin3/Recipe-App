from django.urls import path
from . import views

urlpatterns = [
    path('create-account/',views.CreateUserView.as_view(), name="create_account"),
    path("login/", views.UserLoginView.as_view(), name="login"),
    path('verify-email/', views.VerifyEmailView.as_view(),name="verify_email"),
    path("set-notifications/", views.SetNotitfications.as_view(), name="noti"),
    path("set-language/", views.SetLanguage.as_view(), name="lange"),
    path("retrieve-languages/", views.RetrieveAllLanguages.as_view(), name="all_lang"),
    path("user-detail/<email>/", views.UserDetailView.as_view(), name="user_detail"),
    path("request-password-reset/", views.RequestPasswordResetCode.as_view(), name="req_pass"),
    path("password-reset/", views.PasswordReset.as_view(), name="reset_pass"),
    path("get-payment-methods/<email>/", views.RetrievePaymentMethods.as_view(), name="get_pms"),
    path("get-addresses/<email>/", views.RetrieveAddresses.as_view(), name="get_adds"),
    path("add-payment/", views.AddPaymentMethods.as_view(), name="add_pay"),
    path("add-address/", views.AddAddress.as_view(), name="add_adds"),
    path("all-regions/", views.RetrieveAllRegions.as_view(), name="all_regs"),
]

