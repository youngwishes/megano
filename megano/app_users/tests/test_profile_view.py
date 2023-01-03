from django.urls import reverse
from megano.core.tests.mixins import TestInitialUserDataMixin
from django.test import TestCase


class TestUserProfileView(TestInitialUserDataMixin, TestCase):
    def setUp(self) -> None:
        self.url = reverse('profile')

    def login_basic_user(self):
        username, password = self.get_basic_user()
        self.client.login(username=username, password=password)


    def test_profile_view_access(self):
        self.login_basic_user()
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)

    def test_add_user_profile_data(self):
        self.login_basic_user()
        data = {
            'first_name': 'Danil',
            'last_name': 'Fedorov',
            'phone_number': '+79092981182',
            'bank_card': '1234567890'
        }

        self.client.post(self.url, data=data)

        response = self.client.get(self.url)

        for value in data.values():
            self.assertContains(response, value)

    def test_add_incorrect_phone_number(self):
        self.login_basic_user()

        response = self.client.post(self.url, data={'phone_number': '+7909298118'})
        self.assertContains(response, 'Enter a valid phone number')

        response = self.client.get(self.url)
        self.assertNotContains(response, '+7909298118')
