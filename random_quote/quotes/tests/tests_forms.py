from random import choice
from http import HTTPStatus
from django.test import TestCase
from django.contrib.auth import get_user_model
from django.urls import reverse
from quotes.models import Author, Category, Quote


class QuotesFormsTestCase(TestCase):

    fixtures = [
        "quotes_menu.json",
        "quotes_category.json",
        "quotes_authors.json",
        "quotes_quotes.json",
        "auth_users.json",
    ]

    def setUp(self):
        self.test_user = {
            "username": "new_user",
            "password": "user1234!",
            "email": "new_user@mail.ru",
        }
        self.user = get_user_model().objects.create(
            username=self.test_user["username"],
            email=self.test_user["email"],
            password=self.test_user["password"],
        )

    def test_save_quote_form(self):

        random_quote = choice(Quote.objects.values("pk"))["pk"]
        self.client.force_login(user=self.user)
        self.client.get(reverse("save_quote", kwargs={"id": random_quote}))
        self.assertTrue(
            get_user_model()
            .objects.get(username=self.test_user["username"])
            .profile.saved_quotes.filter(id=random_quote)
            .exists()
        )

    def test_create_quote_form_exist_author(self):

        author = choice(Author.objects.all()).id
        categories = choice(Category.objects.all())
        test_form = {
            "author": author,
            "quote": "Some quote",
            "categories": categories.id,
            "new_categories": "new cat one, new cat two",
        }

        self.client.force_login(user=self.user)

        response = self.client.post(reverse("create_quote"), test_form)
        self.assertTrue(response.status_code, HTTPStatus.OK)
        self.assertTemplateUsed("quotes/success_form.html")
        self.assertTrue(Quote.objects.filter(quote="Some quote").exists())
        self.assertTrue(Quote.objects.get(quote="Some quote").author.id == author)

    def test_create_quote_form_new_author(self):

        categories = choice(Category.objects.all())
        test_form = {
            "new_author": "new author",
            "quote": "Some quote",
            "categories": categories.id,
            "new_categories": "new cat one, new cat two",
        }

        self.client.force_login(user=self.user)

        response = self.client.post(reverse("create_quote"), test_form)
        self.assertTrue(response.status_code, HTTPStatus.OK)
        self.assertTemplateUsed("quotes/success_form.html")
        self.assertTrue(Quote.objects.filter(quote="Some quote").exists())
        self.assertTrue(
            Quote.objects.get(quote="Some quote").author.name == "New Author"
        )

    def test_create_quote_no_auotrs(self):

        categories = choice(Category.objects.all())
        test_form = {
            "quote": "Some quote",
            "categories": categories.id,
            "new_categories": "new cat one, new cat two",
        }

        self.client.force_login(user=self.user)
        response = self.client.post(reverse("create_quote"), test_form)
        self.assertContains(
            response, "Вы должны выбрать автора из списка или написать своего"
        )

    def test_create_quote_no_categories(self):

        author = choice(Author.objects.all()).id
        test_form = {
            "author": author,
            "quote": "Some quote",
        }

        self.client.force_login(user=self.user)
        response = self.client.post(reverse("create_quote"), test_form)
        self.assertContains(
            response, "Вы должны выбрать хотя бы одну категорию или написать свою"
        )

    def test_creste_quote_wrong_categories(self):

        author = choice(Author.objects.all()).id
        test_form = {
            "author": author,
            "quote": "Some quote",
            "new_categories": "category with a digit 1",
        }

        self.client.force_login(user=self.user)
        response = self.client.post(reverse("create_quote"), test_form)
        self.assertContains(
            response,
            "Введите корректное название категорий! Они могут содержать только буквы и пробелы,\
                               а так же должны разделяться запятыми! Их может быть не более 7 штук!",
        )

    def test_create_quote_wrong_author(self):

        test_form = {
            "new_author": "author with a digit 1",
            "quote": "Some quote",
            "new_categories": "category",
        }

        self.client.force_login(user=self.user)
        response = self.client.post(reverse("create_quote"), test_form)
        self.assertContains(
            response,
            "Введите корректное имя автора! Оно должно содержать только буквы и пробелы! А так же дефис, если фамилия двойная.",
        )
