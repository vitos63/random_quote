from django.test import TestCase
from django.contrib.auth import get_user_model
from quotes.models import Author, Category, Quote
from users.services.delete_saved_quote_service import DeleteSavedQuoteService


class DeleteSavedQuoteServiceTestsCase(TestCase):

    def setUp(self):
        self.user = get_user_model().objects.create(
            username="Test User", email="testuser@mail.ru"
        )
        self.author = Author.objects.create(name="Test Author")
        self.category = Category.objects.create(name="Test Category")
        self.quote = Quote.objects.create(quote="Test Quote", author=self.author)
        self.quote.category.add(self.category)
        self.user.profile.saved_quotes.add(self.quote)
        return super().setUp()

    def test_success_delete_quote(self):
        response = DeleteSavedQuoteService(self.quote.id, self.user).delete()
        self.assertTrue(response)

    def test_quote_does_not_exists(self):
        response = DeleteSavedQuoteService(-1, self.user).delete()
        self.assertEqual(response, None)
