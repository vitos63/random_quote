from django.db import models
from quotes.models import Quote
from django.contrib.auth import get_user_model

class Profile(models.Model):
    user = models.OneToOneField(get_user_model(), on_delete=models.CASCADE)
    photo = models.ImageField(upload_to='photos/%Y/%m/%d', verbose_name='Фото', blank=True)
    saved_quotes = models.ManyToManyField(Quote, verbose_name='Сохраненные цитаты', related_name='saved_quotes')


