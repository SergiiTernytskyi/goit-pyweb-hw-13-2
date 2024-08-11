from django.urls import path
from django.contrib.auth.views import (
    LogoutView,
    PasswordResetDoneView,
    PasswordResetConfirmView,
    PasswordResetCompleteView,
)

from . import views
from .forms import SigninForm

app_name = "users"

urlpatterns = [
    path("signup/", views.signupuser, name="signup"),
    path(
        "signin/",
        views.signinuser,
        name="signin",
    ),
    path(
        "signout/",
        LogoutView.as_view(template_name="users/signout.html"),
        name="signout",
    ),
    path("reset-password/", views.ResetPasswordView.as_view(), name="reset-password"),
    path(
        "reset-password/done/",
        PasswordResetDoneView.as_view(template_name="users/password_reset_done.html"),
        name="reset-password-done",
    ),
    path(
        "reset-password/confirm/<uidb64>/<token>/",
        PasswordResetConfirmView.as_view(
            template_name="users/password_reset_confirm.html",
            success_url="/users/reset-password/complete/",
        ),
        name="password_reset_confirm",
    ),
    path(
        "reset-password/complete/",
        PasswordResetCompleteView.as_view(
            template_name="users/password_reset_complete.html"
        ),
        name="password_reset_complete",
    ),
]
