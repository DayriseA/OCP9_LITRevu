# Generated by Django 4.2.6 on 2023-10-20 01:45

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("authentication", "0003_customuser_blocks"),
    ]

    operations = [
        migrations.AddField(
            model_name="customuser",
            name="role",
            field=models.CharField(
                choices=[
                    ("Administrator", "Administrateur"),
                    ("Moderator", "Modérateur"),
                    ("Basic", "Utilisateur"),
                ],
                default="Basic",
                max_length=20,
                verbose_name="Rôle",
            ),
        ),
    ]
