from django.urls import path

from churchill.api.v1.user.views import (
    RegisterView,
    LoginView,
    RegisterVerifyView,
    ResetPasswordView,
    ResetPasswordConfirmView,
)

app_name = "user"


urlpatterns = [
    path("register/", RegisterView.as_view(), name="register"),
    path("register-verify/", RegisterVerifyView.as_view(), name="register_verify"),
    path("login/", LoginView.as_view(), name="login"),
    path("reset-password/", ResetPasswordView.as_view(), name="reset_password"),
    path(
        "reset-password-confirm/",
        ResetPasswordConfirmView.as_view(),
        name="reset_password_confirm",
    ),
]
