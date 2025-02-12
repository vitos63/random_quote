from random import choice
from django.test import TestCase
from django.urls import reverse
from django.contrib.auth import get_user_model
from http import HTTPStatus
from quotes.models import Quote

class UserPagesTestCase(TestCase):
    fixtures = ['quotes_menu.json', 'quotes_category.json', 'quotes_authors.json', 'quotes_quotes.json', 'auth_users.json']

    def setUp(self):

        test_user = {
            'username':'new_user',
            'password':'user1234!',
            'email':'new_user@mail.ru'
        }
        self.user = get_user_model().objects.create(username = test_user['username'], 
                                                    email = test_user['email'], 
                                                    password = test_user['password']
                                                    )

    def test_login_page(self):
        
        response = self.client.get(reverse('users:login'))
        self.assertEqual(response.status_code, HTTPStatus.OK)
        self.assertTemplateUsed('users/login.html')

    def test_login_page_is_authenticated(self):

        redirect_uri = reverse('users:suggested_quotes')
        self.client.force_login(user=self.user)
        response = self.client.get(reverse('users:login'))
        self.assertEqual(response.status_code, HTTPStatus.FOUND)
        self.assertRedirects(response, redirect_uri)
        
    
    def test_logout_page(self):

        redirect_uri = reverse('home')
        self.client.force_login(user=self.user)
        response = self.client.post(reverse('users:logout'))
        self.assertEqual(response.status_code, HTTPStatus.FOUND)
        self.assertRedirects(response, redirect_uri)

    def test_register_page(self):

        response = self.client.get(reverse('users:register'))
        self.assertEqual(response.status_code, HTTPStatus.OK)
        self.assertTemplateUsed('users/register.html')
        self.assertTemplateUsed('users/user_register.html')
    
    def test_suggested_quotes_page(self):

        self.client.force_login(user=self.user)
        response = self.client.get(reverse('users:suggested_quotes'))
        self.assertEqual(response.status_code, HTTPStatus.OK)
        self.assertTemplateUsed(response, 'users/user_suggested_quotes.html')
    
    def test_saved_quotes_page(self):

        self.client.force_login(user=self.user)
        response = self.client.get(reverse('users:saved_quotes'))
        self.assertEqual(response.status_code, HTTPStatus.OK)
        self.assertTemplateUsed(response, 'users/user_saved_quotes.html')
    
    def test_edit_profile_page(self):

        self.client.force_login(user=self.user)
        response = self.client.get(reverse('users:edit_profile'))
        self.assertEqual(response.status_code, HTTPStatus.OK)
        self.assertTemplateUsed(response, 'users/edit_profile.html')



class UserFormTestCase(TestCase):
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
        

    def test_login_form(self):

        test_user_1= {
            'username':'new_user_1',
            'password1':'user1234!',
            'password2':'user1234!',
            'email':'new_user_1@mail.ru'
            }

        redirect_uri = reverse('users:edit_profile')
        path = reverse('users:login')
        response = self.client.post(reverse('users:register'), test_user_1)
        response = self.client.post(path, {'username': test_user_1['username'], 'password': test_user_1['password1']})

        self.assertEqual(response.status_code, HTTPStatus.FOUND)
        self.assertRedirects(response, redirect_uri)
    
    def test_register_form(self):
        
        test_user_1= {
            'username':'new_user_1',
            'password1':'user1234!',
            'password2':'user1234!',
            'email':'new_user_1@mail.ru'
            }

        redirect_uri = reverse('users:login') + '?next=/users/profile/suggested-quotes/'
        path = reverse('users:register')

        response = self.client.post(path, test_user_1, follow=True)
        self.assertEqual(response.status_code, HTTPStatus.OK)
        self.assertRedirects(response, redirect_uri, status_code=302, target_status_code=200)
        self.assertTrue(get_user_model().objects.filter(username = test_user_1['username']).exists())
    
    def test_register_form_errors(self):

        test_user_bad_email = {
            'username':'new_user_2',
            'password1':'user1234!',
            'password2':'user1234!',
            'email':'new_user@mail.ru',
        }

        test_user_bad_username = {
            'username':'new_user',
            'password1':'user1234!',
            'password2':'user1234!',
            'email':'new_user_2@mail.ru',
        }

        response_1 = self.client.post(reverse('users:register'), test_user_bad_email, follow=True)
        self.assertEqual(response_1.status_code, HTTPStatus.OK)
        self.assertFalse(get_user_model().objects.filter(username='new_user_2').exists())
        self.assertContains(response_1, 'Пользователь с таким E-mail уже существует')

        response_2 = self.client.post(reverse('users:register'), test_user_bad_username, follow=True)
        self.assertEqual(response_2.status_code, HTTPStatus.OK)
        self.assertContains(response_2, 'Пользователь с таким именем уже существует')
    
    def test_edit_profile_form(self):

        test_edit_profile_form = {
            'first_name':'test_first_name',
            'last_name':'test_last_name'
        }

        self.client.force_login(user=self.user)
        response = self.client.post(reverse('users:edit_profile'), test_edit_profile_form)
        self.assertEqual(response.status_code, HTTPStatus.FOUND)
        self.assertRedirects(response, reverse('users:edit_profile'))
        self.assertTrue(get_user_model().objects.get(username=self.test_user['username']).first_name,'test_first_name')
        self.assertTrue(get_user_model().objects.get(username=self.test_user['username']).last_name,'test_last_name')
    
    def test_delete_save_quotes(self):

        random_quote = choice(Quote.objects.values('pk'))['pk']

        self.client.force_login(user=self.user)
        self.client.get(reverse('save_quote',kwargs={'id':random_quote}))
        self.assertTrue(get_user_model().objects.get(username=self.test_user['username']).profile.saved_quotes.filter(id=random_quote).exists())
        response = self.client.get(reverse('users:delete_saved_quotes', kwargs={'id':random_quote}))
        self.assertTrue(response.status_code, HTTPStatus.FOUND)
        self.assertRedirects(response, reverse('users:saved_quotes'))
        self.assertFalse(get_user_model().objects.get(username=self.test_user['username']).profile.saved_quotes.filter(id=random_quote).exists())



    

    

