from random import choice
from django.test import TestCase
from django.urls import reverse
from django.db.models import Q, Count
from http import HTTPStatus
from urllib.parse import urlencode
from quotes.models import Author, Category, Quote


class QuoteViewsTestCase(TestCase):
    fixtures = [
        "quotes_menu.json",
        "quotes_category.json",
        "quotes_authors.json",
        "quotes_quotes.json",
        "auth_users.json",
    ]

    def test_home_page(self):

        response = self.client.get(reverse("home"))
        self.assertEqual(response.status_code, HTTPStatus.OK)
        self.assertTemplateUsed("quotes/home.html")

    def test_authors_page(self):

        response = self.client.get(reverse("authors"))
        self.assertEqual(response.status_code, HTTPStatus.OK)
        self.assertTemplateUsed("quotes/authors.html")

    def test_categories_page(self):

        response = self.client.get(reverse("categories"))
        self.assertEqual(response.status_code, HTTPStatus.OK)
        self.assertTemplateUsed("quotes/categories.html")

    def test_author_quotes_page(self):

        for i in Author.objects.all():
            response = self.client.get(
                reverse("author_quotes", kwargs={"author": i.slug})
            )
            self.assertEqual(response.status_code, HTTPStatus.OK)
            self.assertTemplateUsed("quotes/author_quotes.html")

    def test_category_quotes_page(self):

        for i in Category.objects.all():
            response = self.client.get(
                reverse("category_quotes", kwargs={"category": i.slug})
            )
            self.assertEqual(response.status_code, HTTPStatus.OK)
            self.assertTemplateUsed("quotes/author_quotes.html")

    def test_search_page(self):

        data = {"search_field": "человек"}
        response = self.client.get(reverse("search") + "?" + urlencode(data))
        self.assertEqual(response.status_code, HTTPStatus.OK)
        self.assertTemplateUsed("quotes/search.html")
        self.assertEqual(
            list(response.context["quotes_result"]),
            list(
                Quote.objects.filter(
                    quote__icontains=response.context["search_field"],
                    status="Published",
                )
            ),
        )
        self.assertEqual(
            list(response.context["authors_result"]),
            list(
                Author.objects.annotate(
                    published_quotes_count=Count(
                        "author_quotes", filter=Q(author_quotes__status="Published")
                    )
                ).filter(
                    published_quotes_count__gt=0,
                    name__icontains=response.context["search_field"],
                )
            ),
        )
        self.assertEqual(
            list(response.context["categories_result"]),
            list(
                Category.objects.annotate(
                    published_quotes_count=Count(
                        "category_quotes", filter=Q(category_quotes__status="Published")
                    )
                ).filter(
                    published_quotes_count__gt=0,
                    name__icontains=response.context["search_field"],
                )
            ),
        )

    def test_redirect_create_quote_page(self):

        path = reverse("create_quote")
        redirect_uri = reverse("users:login") + "?next=" + path
        response = self.client.get(path)
        self.assertEqual(response.status_code, HTTPStatus.FOUND)
        self.assertRedirects(response, redirect_uri)

    def test_redirect_save_quote_page(self):

        path = reverse("save_quote", kwargs={"id": choice(Quote.objects.all()).id})
        redirect_uri = reverse("users:login") + "?next=" + path
        response = self.client.get(path)
        self.assertEqual(response.status_code, HTTPStatus.FOUND)
        self.assertRedirects(response, redirect_uri)


