"""URL configuration for authentication app."""
from django.urls import path
from django.contrib.auth.views import (
    LoginView,
    LogoutView,
    PasswordChangeView,
    PasswordChangeDoneView,
)
from .forms import MyAuthForm
from . import views

urlpatterns = [
    path("signup/", views.signup, name="signup"),
    path(
        "login/",
        LoginView.as_view(
            template_name="authentication/login.html",
            authentication_form=MyAuthForm,
            redirect_authenticated_user=True,
        ),
        name="login",
    ),
    path("logout/", LogoutView.as_view(), name="logout"),
    path(
        "password_change/",
        PasswordChangeView.as_view(template_name="authentication/password_change.html"),
        name="password_change",
    ),
    path(
        "password_change/done/",
        PasswordChangeDoneView.as_view(
            template_name="authentication/password_change_done.html"
        ),
        name="password_change_done",
    ),
]
