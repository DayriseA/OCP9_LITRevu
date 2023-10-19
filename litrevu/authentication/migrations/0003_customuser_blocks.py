# Generated by Django 4.2.6 on 2023-10-19 12:28

from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("authentication", "0002_customuser_avatar_userfollows_customuser_follows"),
    ]

    operations = [
        migrations.AddField(
            model_name="customuser",
            name="blocks",
            field=models.ManyToManyField(blank=True, to=settings.AUTH_USER_MODEL),
        ),
    ]
