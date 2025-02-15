# Generated by Django 5.1.4 on 2025-01-18 08:26

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('quotes', '0011_alter_quotes_category'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.AddField(
            model_name='quotes',
            name='user',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='suggested_quotes', to=settings.AUTH_USER_MODEL, verbose_name='Пользователь добавивший цитату'),
        ),
    ]
