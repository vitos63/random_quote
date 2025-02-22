from django.test import TestCase
from django.contrib.auth import get_user_model
from quotes.models import Author, Category, Quote
from quotes.services.save_quote_service import SaveQuoteService


class SaveQuoteServiceTestsCase(TestCase):

    def setUp(self):
        self.user = get_user_model().objects.create(
            username="Test User", email="testuser@mail.ru"
        )
        self.author = Author.objects.create(name="Test Author")
        self.category = Category.objects.create(name="Test Category")
        self.quote = Quote.objects.create(quote="Test Quote", author=self.author)
        self.quote.category.add(self.category)
        return super().setUp()

    def test_success_save_quote(self):
        response = SaveQuoteService(self.quote.id, self.user).save_quote()
        self.assertEqual(response, "Цитата успешно сохранена")

    def test_quote_already_saved(self):
        response_success = SaveQuoteService(self.quote.id, self.user).save_quote()
        response_already_saved = SaveQuoteService(self.quote.id, self.user).save_quote()
        self.assertEqual(response_already_saved, "Цитата уже сохранена")

    def test_quote_does_not_exists(self):
        response = SaveQuoteService(-1, self.user).save_quote()
        self.assertEqual(response, None)
