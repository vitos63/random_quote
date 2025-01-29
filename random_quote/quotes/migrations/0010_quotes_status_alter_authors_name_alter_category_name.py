# Generated by Django 5.1.4 on 2025-01-17 06:20

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('quotes', '0009_authors_photo'),
    ]

    operations = [
        migrations.AddField(
            model_name='quotes',
            name='status',
            field=models.CharField(choices=[('Published', 'Опубликована'), ('Rejected', 'Отклонена'), ('Under consideration', 'На рассмотрении')], default='Under consideration', max_length=150, verbose_name='Статус'),
        ),
        migrations.AlterField(
            model_name='authors',
            name='name',
            field=models.CharField(db_index=True, max_length=250, verbose_name='Автор'),
        ),
        migrations.AlterField(
            model_name='category',
            name='name',
            field=models.CharField(db_index=True, max_length=250, verbose_name='Категория'),
        ),
    ]
