from django.test import TestCase
from django.urls import reverse
from rest_framework.test import APIClient
from rest_framework import status
from django.contrib.auth import get_user_model
from quotes.models import Quotes, Authors, Category



class APITestCase(TestCase):
    def setUp(self):
        
        self.client = APIClient()
        self.user = get_user_model().objects.create_user(username='testuser', email='testuser@example.com', password='password123')
        self.author = Authors.objects.create(name='Author 1', slug='author-1')
        self.category = Category.objects.create(name='Category 1', slug='category-1')
        self.quote = Quotes.objects.create(quote='Test Quote', author=self.author, status='Published')
        self.quote.category.add(self.category)

    def test_random_quote_api_view(self):

        url = reverse('api_quotes:random_quote')
        response = self.client.get(url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('quote', response.data)
        self.assertIn('category', response.data)
        self.assertIn('author', response.data)
        self.assertEqual(response.data['quote'], self.quote.quote)
        self.assertEqual(response.data['author'], self.quote.author.name)

    def test_authors_api_view(self):

        url = reverse('api_quotes:authors')
        response = self.client.get(url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.data[0]['name'], 'Author 1')

    def test_categories_api_view(self):

        url = reverse('api_quotes:categories')
        response = self.client.get(url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.data[0]['name'], 'Category 1')

    def test_author_quotes_api_view(self):

        url = reverse('api_quotes:author_quotes', kwargs={'author': self.author.slug})
        response = self.client.get(url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.data[0]['quote'], 'Test Quote')

    def test_search_api_view_quote(self):

        url = reverse('api_quotes:search')
        response = self.client.get(url, {'search_field': 'Test'})

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('quotes_result', response.data)
        self.assertEqual(len(response.data['quotes_result']), 1)
        self.assertEqual(response.data['quotes_result'][0]['quote'], 'Test Quote')

    def test_search_api_view_author(self):

        url = reverse('api_quotes:search')
        response = self.client.get(url, {'search_field': 'au'})

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('quotes_result', response.data)
        self.assertEqual(len(response.data['authors_result']), 1)
        self.assertEqual(response.data['authors_result'][0]['name'], 'Author 1')
    
    def test_search_api_view_category(self):

        url = reverse('api_quotes:search')
        response = self.client.get(url, {'search_field': 'cat'})

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('quotes_result', response.data)
        self.assertEqual(len(response.data['categories_result']), 1)
        self.assertEqual(response.data['categories_result'][0]['name'], 'Category 1')
    
    def test_search_api_view_author_and_category(self):

        url = reverse('api_quotes:search')
        response = self.client.get(url, {'search_field': '1'})

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('quotes_result', response.data)
        self.assertEqual(len(response.data['categories_result']), 1)
        self.assertEqual(len(response.data['authors_result']), 1)
        self.assertEqual(response.data['categories_result'][0]['name'], 'Category 1')
        self.assertEqual(response.data['authors_result'][0]['name'], 'Author 1')

    def test_create_quote_api_view(self):

        self.client.force_authenticate(user=self.user)
        url = reverse('api_quotes:create_quote')
        data = {
            'quote': 'New Quote',
            'author': self.author.id,
            'categories': [self.category.id],
        }
        response = self.client.post(url, data)

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data['quote'], 'New Quote')

    def test_create_quote_new_author_api_view(self):

        self.client.force_authenticate(user=self.user)
        url = reverse('api_quotes:create_quote')
        data = {
            'quote': 'New Quote',
            'new_author': 'New Author',
            'categories': [self.category.id],
        }
        response = self.client.post(url, data)

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data['author'],'New Author')
    
    def test_create_quote_new_categories_api_view(self):

        self.client.force_authenticate(user=self.user)
        url = reverse('api_quotes:create_quote')
        data = {
            'quote': 'New Quote',
            'new_author': 'New Author',
            'new_categories': 'New_cat_1, New_cat_2'
        }
        response = self.client.post(url, data)

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data['category'], data['new_categories'].split(', '))
    
    def test_create_quote_author_error_api_view(self):

        data = {
            'quote': 'New Quote',
            'new_categories': 'New_cat_1, New_cat_2'
        }

        self.client.force_authenticate(user=self.user)
        url = reverse('api_quotes:create_quote')
        response = self.client.post(url, data)

        self.assertTrue(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertTrue(response.data['author'], 'Вы должны выбрать уже существующего автора или написать своего')
    
    def test_create_quote_categories_error_api_view(self):

        data = {
            'quote': 'New Quote',
            'new_author' : 'New Author'
        }
        
        self.client.force_authenticate(user=self.user)
        url = reverse('api_quotes:create_quote')
        response = self.client.post(url, data)

        self.assertTrue(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertTrue(response.data['categories'], 'Вы должны выбрать из уже существующих категорий или написать свои')


    def test_saved_quotes_api_view(self):

        self.user.profile.saved_quotes.add(self.quote)

        self.client.force_authenticate(user=self.user)
        url = reverse('api_quotes:saved_quotes')
        response = self.client.get(url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.data[0]['quote'], 'Test Quote')
