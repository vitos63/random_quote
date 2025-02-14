from django.db import models
from django.urls import reverse
from django.contrib.auth import get_user_model
from slugify import slugify
from quotes.managers import AuthorManager, CategoryManager, QuoteManager

User = get_user_model()


class Menu(models.Model):

    title = models.CharField(max_length=150, verbose_name="Меню")
    url_name = models.CharField(max_length=100, verbose_name="Эндпоинт")

    def __str__(self):
        return self.title


class Quote(models.Model):
    quote = models.TextField(verbose_name="Цитата", db_index=True)
    author = models.ForeignKey(
        "Author",
        on_delete=models.CASCADE,
        related_name="author_quotes",
        verbose_name="Автор",
    )
    category = models.ManyToManyField(
        "Category", related_name="category_quotes", verbose_name="Категории"
    )
    status = models.CharField(
        max_length=150,
        verbose_name="Статус",
        choices={
            "Published": "Опубликована",
            "Rejected": "Отклонена",
            "Under consideration": "На рассмотрении",
        },
        default="Under consideration",
    )
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="suggested_quotes",
        verbose_name="Пользователь добавивший цитату",
        blank=True,
        null=True,
    )
    objects = QuoteManager()

    def __str__(self):
        return self.quote


class Author(models.Model):
    name = models.CharField(max_length=250, verbose_name="Автор", db_index=True)
    biography = models.TextField(verbose_name="Биография", default="some information")
    slug = models.SlugField(max_length=250, unique=True, verbose_name="Слаг")
    photo = models.ImageField(
        upload_to="photos/%Y/%m/%d", verbose_name="Фото автора", blank=True
    )
    objects = AuthorManager()

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        self.slug = slugify(self.name)
        return super().save(*args, **kwargs)

    def get_absolute_url(self):
        return reverse("author_quotes", kwargs={"author": self.slug})


class Category(models.Model):
    name = models.CharField(max_length=250, verbose_name="Категория", db_index=True)
    slug = models.SlugField(max_length=250, unique=True, verbose_name="Слаг")
    objects = CategoryManager()

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        self.slug = slugify(self.name)
        return super().save(*args, **kwargs)

    def get_absolute_url(self):
        return reverse("category_quotes", kwargs={"category": self.slug})
