from django.test import TestCase
from django.urls import reverse
from django.contrib.auth.models import User
from .models import Tourist


class AuthTests(TestCase):
    def setUp(self):
        # create a user with a normal username and a phone profile
        self.phone = '9812345678'
        self.username = 'testuser'
        self.password = 'pa ss@word'  # include spaces and special chars to ensure no stripping
        self.user = User.objects.create_user(username=self.username, password=self.password, first_name='Test')
        Tourist.objects.create(user=self.user, phone=self.phone)

    def test_login_with_username(self):
        response = self.client.post(reverse('login'), {
            'identifier': self.username,
            'password': self.password
        })
        # on success should redirect to dashboard
        self.assertEqual(response.status_code, 302)
        self.assertEqual(response.url, reverse('dashboard'))

    def test_login_with_plain_phone(self):
        response = self.client.post(reverse('login'), {
            'identifier': self.phone,
            'password': self.password
        })
        self.assertEqual(response.status_code, 302)
        self.assertEqual(response.url, reverse('dashboard'))

    def test_login_with_formatted_phone(self):
        formatted = '98-1234 5678'
        response = self.client.post(reverse('login'), {
            'identifier': formatted,
            'password': self.password
        })
        self.assertEqual(response.status_code, 302)
        self.assertEqual(response.url, reverse('dashboard'))

    def test_login_invalid_credentials(self):
        response = self.client.post(reverse('login'), {
            'identifier': self.phone,
            'password': 'wrongpass'
        })
        # should return 200 and show form with error
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Invalid credentials')

    def test_signup_redirects_to_login_and_saves_phone_as_username(self):
        data = {
            'name': 'New User',
            'email': 'new@example.com',
            'phone_number': '9812345679',
            'password1': 'pa ss@word',
            'password2': 'pa ss@word'
        }
        response = self.client.post(reverse('signup'), data)
        # on success should redirect to login (no auto-login)
        self.assertEqual(response.status_code, 302)
        self.assertEqual(response.url, reverse('login'))

        # verify that the user was created and username == phone
        from django.contrib.auth.models import User
        u = User.objects.get(email='new@example.com')
        self.assertEqual(u.username, '9812345679')
        self.assertEqual(u.first_name, 'New User')

        # Now, login with phone and password should work
        resp2 = self.client.post(reverse('login'), {'identifier': '9812345679', 'password': 'pa ss@word'})
        # login redirects to dashboard when phone present
        self.assertEqual(resp2.status_code, 302)
        self.assertEqual(resp2.url, reverse('dashboard'))

    def test_post_login_redirects_to_complete_profile_when_phone_missing(self):
        from django.contrib.auth.models import User
        user = User.objects.create_user(username='nopho', password='x', first_name='NoPhone')
        # ensure tourist exists with empty phone
        from .models import Tourist
        Tourist.objects.create(user=user, phone='')

        # login
        login = self.client.login(username='nopho', password='x')
        self.assertTrue(login)
        resp = self.client.get(reverse('post_login'))
        self.assertEqual(resp.status_code, 302)
        self.assertEqual(resp.url, reverse('complete_profile'))

    def test_social_signup_signal_creates_tourist(self):
        from allauth.account.signals import user_signed_up
        from django.contrib.auth.models import User

        user = User.objects.create_user(username='socialuser', password='x', email='s@example.com')
        # ensure no Tourist initially
        from .models import Tourist
        self.assertFalse(Tourist.objects.filter(user=user).exists())

        class DummyAccount:
            extra_data = {'phone': '9812345000'}

        class DummySocialLogin:
            account = DummyAccount()

        # send signal
        user_signed_up.send(sender=User, request=None, user=user, sociallogin=DummySocialLogin())

        # user should now have a Tourist
        t = Tourist.objects.get(user=user)
        self.assertEqual(t.phone, '9812345000')
