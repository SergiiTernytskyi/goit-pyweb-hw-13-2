from django.contrib import messages
from django.shortcuts import render, redirect
from django.views import View

from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.views import (
    PasswordResetView,
    PasswordResetDoneView,
    PasswordResetConfirmView,
    PasswordResetCompleteView,
)

from django.contrib.messages.views import SuccessMessageMixin
from django.urls import reverse_lazy

from .forms import SignupForm, SigninForm


def signupuser(request):
    if request.user.is_authenticated:
        return redirect(to="quotes_app:root")

    if request.method == "POST":
        form = SignupForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect(to="quotes_app:root")
        else:
            return render(request, "users/signup.html", context={"form": form})

    return render(request, "users/signup.html", context={"form": SignupForm()})


def signinuser(request):
    if request.user.is_authenticated:
        return redirect("root")

    if request.method == "POST":
        user = authenticate(
            username=request.POST["username"], password=request.POST["password"]
        )
        if user is None:
            messages.error(request, "Username or password didn't match")
            return redirect(to="users:login")

        signin(request, user)
        return redirect(to="quotes_app:root")

    return render(request, "users/signin.html", context={"form": SigninForm()})


class ResetPasswordView(SuccessMessageMixin, PasswordResetView):
    template_name = "users/password_reset.html"
    email_template_name = "users/password_reset_email.html"
    html_email_template_name = "users/password_reset_email.html"
    success_url = reverse_lazy("users:reset-password-done")
    success_message = (
        "An email with instructions to reset your password has been sent to %(email)s."
    )
    subject_template_name = "users/password_reset_subject.txt"
