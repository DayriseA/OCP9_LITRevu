from django.conf import settings
from django.contrib.auth.models import AbstractUser, Group
from django.db import models


def get_avatar_path(instance, filename):
    return f"user_{instance.id}/avatars/{filename}"


# role, groups and avatar not used yet at this point of the project
class CustomUser(AbstractUser):
    ADMINISTRATOR = "Administrator"
    MODERATOR = "Moderator"
    BASIC = "Basic"
    ROLE_CHOICES = (
        (ADMINISTRATOR, "Administrateur"),
        (MODERATOR, "Modérateur"),
        (BASIC, "Utilisateur"),
    )

    role = models.CharField(
        max_length=20,
        choices=ROLE_CHOICES,
        default=BASIC,
        verbose_name="Rôle",
    )

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

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        if self.role == self.ADMINISTRATOR:
            self.is_staff = True
            group = Group.objects.get(name="administrators")
            self.groups.add(group)  # equivalent to group.user_set.add(self)
        elif self.role == self.MODERATOR:
            group = Group.objects.get(name="moderators")
            self.groups.add(group)
        elif self.role == self.BASIC:
            group = Group.objects.get(name="basic")
            self.groups.add(group)


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
