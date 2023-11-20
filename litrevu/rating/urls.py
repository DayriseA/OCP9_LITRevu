"""URL configuration for rating app."""
from django.urls import path
from . import views

urlpatterns = [
    path("feed/", views.feed, name="feed"),
    path("my_posts/", views.my_posts, name="my_posts"),
    path("ticket/create/", views.ticket_create, name="ticket_create"),
    path("ticket/<int:ticket_id>/edit/", views.ticket_edit, name="ticket_edit"),
    path(
        "ticket/<int:ticket_id>/respond/",
        views.review_create,
        name="ticket_respond",
    ),
    path("ticket/delete/", views.ticket_delete, name="ticket_delete"),
    path("review/create/", views.review_create, name="review_create"),
    path("review/<int:review_id>/edit/", views.review_edit, name="review_edit"),
    path("review/delete/", views.review_delete, name="review_delete"),
    path("follows/", views.follows, name="follows"),
    path("unfollow/<int:user_id>/", views.unfollow, name="unfollow"),
    path("block/<int:user_id>/", views.block_user, name="block"),
    path("unblock/<int:user_id>/", views.unblock_user, name="unblock"),
]
