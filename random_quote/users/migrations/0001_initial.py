# Generated by Django 5.1.5 on 2025-01-22 06:52

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ("quotes", "0014_alter_quotes_quote"),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name="Profile",
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
                    "photo",
                    models.ImageField(
                        blank=True, upload_to="photos/%Y/%m/%d", verbose_name="Фото"
                    ),
                ),
                (
                    "saved_quotes",
                    models.ManyToManyField(
                        related_name="saved_quotes",
                        to="quotes.quotes",
                        verbose_name="Сохраненные цитаты",
                    ),
                ),
                (
                    "user",
                    models.OneToOneField(
                        on_delete=django.db.models.deletion.CASCADE,
                        to=settings.AUTH_USER_MODEL,
                    ),
                ),
            ],
        ),
    ]
