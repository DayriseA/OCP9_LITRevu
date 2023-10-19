# Generated by Django 4.2.6 on 2023-10-19 11:43

import authentication.models
from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):
    dependencies = [
        ("authentication", "0001_initial"),
    ]

    operations = [
        migrations.AddField(
            model_name="customuser",
            name="avatar",
            field=models.ImageField(
                blank=True,
                null=True,
                upload_to=authentication.models.get_avatar_path,
                verbose_name="Avatar",
            ),
        ),
        migrations.CreateModel(
            name="UserFollows",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                (
                    "followed_user",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="followed_by",
                        to=settings.AUTH_USER_MODEL,
                    ),
                ),
                (
                    "user",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="following",
                        to=settings.AUTH_USER_MODEL,
                    ),
                ),
            ],
            options={
                "unique_together": {("user", "followed_user")},
            },
        ),
        migrations.AddField(
            model_name="customuser",
            name="follows",
            field=models.ManyToManyField(
                blank=True,
                related_name="followers",
                through="authentication.UserFollows",
                to=settings.AUTH_USER_MODEL,
                verbose_name="suit",
            ),
        ),
    ]
