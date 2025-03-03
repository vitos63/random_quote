# Generated by Django 5.1.4 on 2024-12-12 12:56

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Authors',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=250, verbose_name='Автор')),
            ],
        ),
        migrations.CreateModel(
            name='Category',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=250, verbose_name='Категория')),
            ],
        ),
        migrations.CreateModel(
            name='Quotes',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('quote', models.TextField(verbose_name='Цитата')),
                ('author', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='quotes', to='quotes.authors', verbose_name='Автор')),
                ('category', models.ManyToManyField(related_name='Категории', to='quotes.category', verbose_name='quotes')),
            ],
        ),
    ]
