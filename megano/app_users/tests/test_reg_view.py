from django.urls import reverse
from django.test import TestCase
from django.contrib.auth import get_user_model

User = get_user_model()

class TestUserRegisterView(TestCase):
    def setUp(self) -> None:
        self.url = reverse('register')
        self.redirect_url = reverse('profile')
        self.password = User.objects.make_random_password()

        self.register_data = {
            'username': 'youngWishes',
            'password1': self.password,
            'password2': self.password,
            'email': 'youngWishes@back.com',
        }


    def test_register_if_fields_are_valid(self):
        response = self.client.post(self.url, data=self.register_data)

        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, self.redirect_url)

    def test_register_if_not_username(self):
        self.register_data.pop('username')
        response = self.client.post(self.url, data=self.register_data)
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'This field is required.')

    def test_register_if_passwords_are_not_similar(self):
        self.register_data['password2'] += '1'
        response = self.client.post(self.url, data=self.register_data)
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "The two password fields")

    def test_profile_data_with_full_register_data(self):
        self.register_data['first_name'] = 'Danil'
        self.register_data['last_name'] = 'Fedorov'
        self.client.post(self.url, data=self.register_data)

        response = self.client.get(self.redirect_url)

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Danil')
        self.assertContains(response, 'Fedorov')
