from django.test import SimpleTestCase
from django.urls import reverse, resolve

from accounts import views


class TestUrls(SimpleTestCase):
    def test_register(self):
        url = reverse('accounts:user_register')
        self.assertEqual(resolve(url).func.view_class, views.UserRegister)

    def test_forgot_password(self):
        url = reverse('accounts:user_forgot_password')
        self.assertEqual(resolve(url).func.view_class, views.ForgotPassword)

    def test_ResetPassword(self):
        url = reverse('accounts:user_reset_password')
        self.assertEqual(resolve(url).func.view_class, views.ResetPassword)

    def test_profile(self):
        url = reverse('accounts:user_profile')
        self.assertEqual(resolve(url).func.view_class, views.UserProfile)

    def test_change_password(self):
        url = reverse('accounts:user_change_password')
        self.assertEqual(resolve(url).func.view_class, views.ChangePassword)

    def test_change_username(self):
        url = reverse('accounts:user_change_username')
        self.assertEqual(resolve(url).func.view_class, views.ChangeUsername)

    def test_logout(self):
        url = reverse('accounts:user_logout')
        self.assertEqual(resolve(url).func.view_class, views.UserLogout)
