from django.conf import settings
from django.db import models
from django.contrib.auth.models import AbstractUser


def get_avatar_path(instance, filename):
    return f"user_{instance.id}/avatars/{filename}"


class CustomUser(AbstractUser):
    avatar = models.ImageField(
        upload_to=get_avatar_path, verbose_name="Avatar", null=True, blank=True
    )
    follows = models.ManyToManyField(
        settings.AUTH_USER_MODEL,
        through="UserFollows",
        related_name="followers",
        verbose_name="suit",
        symmetrical=False,
        blank=True,
    )
    blocks = models.ManyToManyField(
        settings.AUTH_USER_MODEL,
        blank=True,
    )


class UserFollows(models.Model):
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="following",
    )
    followed_user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="followed_by",
    )

    class Meta:
        unique_together = ("user", "followed_user")
