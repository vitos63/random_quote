from django.db import models
from slugify import slugify
from django.urls import reverse
from django.contrib.auth import get_user_model
from .managers import AuthorManager, CategoryManager

class Menu(models.Model):

    title = models.CharField(max_length=150, verbose_name='Меню')
    url_name = models.CharField(max_length=100, verbose_name='Эндпоинт')

    def __str__(self):
        return self.title


class Quotes(models.Model):
    quote = models.TextField(verbose_name='Цитата', db_index=True)
    author = models.ForeignKey('Authors', on_delete=models.CASCADE, related_name='quotes', verbose_name='Автор')
    category = models.ManyToManyField('Category',related_name='category', verbose_name='quotes')
    status = models.CharField(max_length=150, verbose_name='Статус', 
                              choices={'Published':'Опубликована','Rejected':'Отклонена','Under consideration':'На рассмотрении'}, 
                              default='Under consideration')
    user = models.ForeignKey(get_user_model(), on_delete=models.CASCADE, related_name='suggested_quotes', 
                             verbose_name='Пользователь добавивший цитату', blank=True, null= True)


    def __str__(self):
        return self.quote


class Authors(models.Model):
    name = models.CharField(max_length=250, verbose_name='Автор', db_index=True)
    biography = models.TextField(verbose_name='Биография', default='some information')
    slug = models.SlugField(max_length=250, unique=True, verbose_name='Слаг')
    photo = models.ImageField(upload_to='photos/%Y/%m/%d',verbose_name='Фото автора', blank=True)
    objects = AuthorManager()

    def __str__(self):
        return self.name
    
    def save(self,*args, **kwargs):
        self.slug = slugify(self.name)
        return super().save(*args, **kwargs)
    
    def get_absolute_url(self):
        return reverse('author_quotes', kwargs ={'author':self.slug})


class Category(models.Model):
    name = models.CharField(max_length=250, verbose_name='Категория',  db_index=True)
    slug = models.SlugField(max_length=250, unique=True, verbose_name='Слаг')
    objects = CategoryManager()

    def __str__(self):
        return self.name
    
    def save(self,*args, **kwargs):
        self.slug = slugify(self.name)
        return super().save(*args, **kwargs)
    
    def get_absolute_url(self):
        return reverse('category_quotes', kwargs ={'category':self.slug})