from django.urls import reverse
from megano.core.tests.mixins import TestInitialUserDataMixin
from django.test import TestCase


class TestUserAuthView(TestInitialUserDataMixin, TestCase):

    def setUp(self) -> None:
        self.url = reverse('login')
        self.redirect_url = reverse('profile')


    def test_login_not_registered_user(self):
        username = "Test"
        password = "test_password"
        response = self.client.post(self.url, data={'username': username, 'password': password})

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Please enter a correct username and password.')
        self.assertTemplateUsed(response, 'app_users/login.html')

    def test_login_registered_user(self):
        username, password = self.get_basic_user()
        response = self.client.post(self.url, data={'username': username, 'password': password})
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, self.redirect_url)
