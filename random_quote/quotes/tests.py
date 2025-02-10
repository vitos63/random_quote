from random import choice
from django.test import TestCase
from django.urls import reverse
from django.db.models import Q, Count
from django.contrib.auth import get_user_model
from http import HTTPStatus
from urllib.parse import urlencode
from quotes.models import Authors, Category, Quotes

class QuotePagesTestCase(TestCase):
    fixtures = ['quotes_menu.json', 'quotes_category.json', 'quotes_authors.json', 'quotes_quotes.json', 'auth_users.json']

    def test_home_page(self):

        response = self.client.get(reverse('home'))
        self.assertEqual(response.status_code, HTTPStatus.OK)
        self.assertTemplateUsed('quotes/home.html')
    
    def test_authors_page(self):

        response = self.client.get(reverse('authors'))
        self.assertEqual(response.status_code, HTTPStatus.OK)
        self.assertTemplateUsed('quotes/authors.html')
    
    def test_categories_page(self):

        response = self.client.get(reverse('categories'))
        self.assertEqual(response.status_code, HTTPStatus.OK)
        self.assertTemplateUsed('quotes/categories.html')
    
    def test_author_quotes_page(self):

        for i in Authors.objects.all():
            response = self.client.get(reverse('author_quotes', kwargs={'author':i.slug}))
            self.assertEqual(response.status_code, HTTPStatus.OK)
            self.assertTemplateUsed('quotes/author_quotes.html')
    
    def test_category_quotes_page(self):

        for i in Category.objects.all():
            response = self.client.get(reverse('category_quotes', kwargs={'category':i.slug}))
            self.assertEqual(response.status_code, HTTPStatus.OK)
            self.assertTemplateUsed('quotes/author_quotes.html')
    
    def test_search_page(self):

        data = {'search_field':'человек'}
        response = self.client.get(reverse('search') + '?' + urlencode(data))
        self.assertEqual(response.status_code, HTTPStatus.OK)
        self.assertTemplateUsed('quotes/search.html')
        self.assertEqual(list(response.context['quotes_result']), 
                         list(Quotes.objects.filter(quote__icontains=response.context['search_field'], status='Published')))
        self.assertEqual(list(response.context['authors_result']), 
                         list(Authors.objects.annotate(published_quotes_count = Count('author_quotes',
                                        filter=Q(author_quotes__status='Published'))).filter(published_quotes_count__gt=0, 
                                                                name__icontains=response.context['search_field'])))
        self.assertEqual(list(response.context['categories_result']), 
                         list(Category.objects.annotate(published_quotes_count = Count('category_quotes', 
                                        filter=Q(category_quotes__status='Published'))).filter(published_quotes_count__gt=0,
                                                                name__icontains=response.context['search_field'])))
        
    def test_redirect_create_quote_page(self):

        path = reverse('create_quote')
        redirect_uri = reverse('users:login') + '?next=' + path
        response = self.client.get(path)
        self.assertEqual(response.status_code, HTTPStatus.FOUND)
        self.assertRedirects(response, redirect_uri)
    
    def test_redirect_save_quote_page(self):

        path = reverse('save_quote', kwargs={'id':choice(Quotes.objects.all()).id})
        redirect_uri = reverse('users:login') + '?next=' + path
        response = self.client.get(path)
        self.assertEqual(response.status_code, HTTPStatus.FOUND)
        self.assertRedirects(response, redirect_uri)


class QuotesFormsTestCase(TestCase):

    fixtures = ['quotes_menu.json', 'quotes_category.json', 'quotes_authors.json', 'quotes_quotes.json', 'auth_users.json']

    def setUp(self):
        self.test_user = {
            'username':'new_user',
            'password':'user1234!',
            'email':'new_user@mail.ru'
            }
        self.user = get_user_model().objects.create(username = self.test_user['username'], 
                                                    email = self.test_user['email'], 
                                                    password = self.test_user['password']
                                                    )

    def test_save_quote_form(self):

        random_quote = choice(Quotes.objects.values('pk'))['pk']
        self.client.force_login(user=self.user)
        self.client.get(reverse('save_quote',kwargs={'id':random_quote}))
        self.assertTrue(get_user_model().objects.get(username=self.test_user['username']).profile.saved_quotes.filter(id=random_quote).exists())
    
    def test_create_quote_form_exist_author(self):

        author = choice(Authors.objects.all()).id
        categories = choice(Category.objects.all())
        test_form = {
            'author' : author,
            'quote' : 'Some quote',
            'categories' : categories.id,
            'new_categories':'new_cat1, new_cat2'
        }

        self.client.force_login(user=self.user)

        response = self.client.post(reverse('create_quote'), test_form)
        self.assertTrue(response.status_code, HTTPStatus.OK)
        self.assertTemplateUsed('quotes/success_form.html')
        self.assertTrue(Quotes.objects.filter(quote = 'Some quote').exists())
        self.assertTrue(Quotes.objects.get(quote = 'Some quote').author.id==author)
    
    def test_create_quote_form_new_author(self):

        categories = choice(Category.objects.all())
        test_form = {
            'new_author' : 'new author',
            'quote' : 'Some quote',
            'categories' : categories.id,
            'new_categories':'new_cat1, new_cat2'
        }

        self.client.force_login(user=self.user)

        response = self.client.post(reverse('create_quote'), test_form)
        self.assertTrue(response.status_code, HTTPStatus.OK)
        self.assertTemplateUsed('quotes/success_form.html')
        self.assertTrue(Quotes.objects.filter(quote = 'Some quote').exists())
        self.assertTrue(Quotes.objects.get(quote = 'Some quote').author.name=='New Author')
    
    def test_creste_quote_no_auotrs(self):

        categories = choice(Category.objects.all())
        test_form = {
            'quote' : 'Some quote',
            'categories' : categories.id,
            'new_categories':'new_cat1, new_cat2'
        }
        
        self.client.force_login(user=self.user)
        response = self.client.post(reverse('create_quote'),test_form)
        self.assertContains(response, 'Вы должны выбрать автора из списка или написать своего')
    
    def test_creste_quote_no_categories(self):

        author = choice(Authors.objects.all()).id
        test_form = {
            'author' : author,
            'quote' : 'Some quote',
        }
        
        self.client.force_login(user=self.user)
        response = self.client.post(reverse('create_quote'),test_form)
        self.assertContains(response, 'Вы должны выбрать хотя бы одну категорию или написать свою')

