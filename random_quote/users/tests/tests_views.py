from random import choice
from http import HTTPStatus
from django.test import TestCase
from django.urls import reverse
from django.contrib.auth import get_user_model
from quotes.models import Quote


class UserPagesTestCase(TestCase):
    fixtures = [
        "quotes_menu.json",
        "quotes_category.json",
        "quotes_authors.json",
        "quotes_quotes.json",
        "auth_users.json",
    ]

    def setUp(self):

        test_user = {
            "username": "new_user",
            "password": "user1234!",
            "email": "new_user@mail.ru",
        }
        self.user = get_user_model().objects.create(
            username=test_user["username"],
            email=test_user["email"],
            password=test_user["password"],
        )

    def test_login_page(self):

        response = self.client.get(reverse("users:login"))
        self.assertEqual(response.status_code, HTTPStatus.OK)
        self.assertTemplateUsed("users/login.html")

    def test_login_page_is_authenticated(self):

        redirect_uri = reverse("users:suggested_quotes")
        self.client.force_login(user=self.user)
        response = self.client.get(reverse("users:login"))
        self.assertEqual(response.status_code, HTTPStatus.FOUND)
        self.assertRedirects(response, redirect_uri)

    def test_logout_page(self):

        redirect_uri = reverse("home")
        self.client.force_login(user=self.user)
        response = self.client.post(reverse("users:logout"))
        self.assertEqual(response.status_code, HTTPStatus.FOUND)
        self.assertRedirects(response, redirect_uri)

    def test_register_page(self):

        response = self.client.get(reverse("users:register"))
        self.assertEqual(response.status_code, HTTPStatus.OK)
        self.assertTemplateUsed("users/register.html")
        self.assertTemplateUsed("users/user_register.html")

    def test_suggested_quotes_page(self):

        self.client.force_login(user=self.user)
        response = self.client.get(reverse("users:suggested_quotes"))
        self.assertEqual(response.status_code, HTTPStatus.OK)
        self.assertTemplateUsed(response, "users/user_suggested_quotes.html")

    def test_saved_quotes_page(self):

        self.client.force_login(user=self.user)
        response = self.client.get(reverse("users:saved_quotes"))
        self.assertEqual(response.status_code, HTTPStatus.OK)
        self.assertTemplateUsed(response, "users/user_saved_quotes.html")

    def test_edit_profile_page(self):

        self.client.force_login(user=self.user)
        response = self.client.get(reverse("users:edit_profile"))
        self.assertEqual(response.status_code, HTTPStatus.OK)
        self.assertTemplateUsed(response, "users/edit_profile.html")

    def test_delete_saved_quote(self):

        random_quote = choice(Quote.objects.values("pk"))["pk"]

        self.client.force_login(user=self.user)
        self.client.get(reverse("save_quote", kwargs={"id": random_quote}))
        self.assertTrue(
            get_user_model()
            .objects.get(username=self.test_user["username"])
            .profile.saved_quotes.filter(id=random_quote)
            .exists()
        )
        response = self.client.get(
            reverse("users:delete_saved_quote", kwargs={"id": random_quote})
        )
        self.assertTrue(response.status_code, HTTPStatus.FOUND)
        self.assertRedirects(response, reverse("users:saved_quotes"))
        self.assertFalse(
            get_user_model()
            .objects.get(username=self.test_user["username"])
            .profile.saved_quotes.filter(id=random_quote)
            .exists()
        )
