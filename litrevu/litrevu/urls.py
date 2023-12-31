"""
URL configuration for litrevu project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.contrib.auth.views import (
    LoginView,
    LogoutView,
    PasswordChangeView,
    PasswordChangeDoneView,
)
from django.urls import path

import authentication.views
import rating.views
from authentication.forms import MyAuthForm


urlpatterns = [
    path("admin/", admin.site.urls),
    path("signup/", authentication.views.signup, name="signup"),
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
    path("feed/", rating.views.feed, name="feed"),
    path("my_posts/", rating.views.my_posts, name="my_posts"),
    path("ticket/create/", rating.views.ticket_create, name="ticket_create"),
    path("ticket/<int:ticket_id>/edit/", rating.views.ticket_edit, name="ticket_edit"),
    path(
        "ticket/<int:ticket_id>/respond/",
        rating.views.review_create,
        name="ticket_respond",
    ),
    path(
        "ticket/<int:ticket_id>/delete/",
        rating.views.ticket_delete,
        name="ticket_delete",
    ),
    path("review/create/", rating.views.review_create, name="review_create"),
    path("review/<int:review_id>/edit/", rating.views.review_edit, name="review_edit"),
    path(
        "review/<int:review_id>/delete/",
        rating.views.review_delete,
        name="review_delete",
    ),
    path("follows/", rating.views.follows, name="follows"),
    path("unfollow/<int:user_id>/", rating.views.unfollow, name="unfollow"),
    path("block/<int:user_id>/", rating.views.block_user, name="block"),
    path("unblock/<int:user_id>/", rating.views.unblock_user, name="unblock"),
]

# Do not use this in production.
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
