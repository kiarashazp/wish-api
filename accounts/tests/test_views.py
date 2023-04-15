from django.urls import reverse
from django.test import TestCase, Client
from rest_framework.test import APITestCase

from accounts.models import User


class TestUserRegisterView(TestCase):
    def test_client_POST_valid(self):
        self.client = Client()
        response = self.client.post(reverse("accounts:user_register"),
                                    data={
                                        'username': 'bob',
                                        'email': 'bob@gmail.com',
                                        'password': '1234',
                                        'confirm_password': '1234'
                                    })
        self.assertEqual(response.status_code, 201)
        self.assertEqual(User.objects.count(), 1)

    def test_client_POST_invalid(self):
        response = self.client.post(reverse("accounts:user_register"),
                                    data={
                                        'username': 'bob',
                                        'email': 'invalid',
                                        'password': '1234',
                                        'confirm_password': '1234'
                                    })
        self.assertEqual(response.status_code, 400)


class TestChangeUsername(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='bob', email='bob@gmail.com', password='1234')
        self.client = Client()
        self.res = self.client.post(path=reverse('accounts:user_login'),
                                    username=self.user.email,
                                    password=self.user.password)

    def test_client_UPDATE_valid(self):
        response = self.client.post(reverse("accounts:user_change_username"),
                                    data={
                                        'username': self.user.username,
                                        'new_username': 'kia',
                                    })
        self.assertEqual(response.status_code, 202)
