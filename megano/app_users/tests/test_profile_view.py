from django.urls import reverse
from megano.core.tests.mixins import TestInitialUserDataMixin
from django.test import TestCase
from megano.core.loading import get_model

Profile = get_model('user', 'Profile')


class TestUserProfileView(TestInitialUserDataMixin, TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.set_up_user_data()

    def setUp(self) -> None:
        self.url = reverse('profile')
        self.login_basic_user()

    def login_basic_user(self):
        username, password = self.get_basic_user()
        self.client.login(username=username, password=password)

    def test_profile_view_access(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)

    def test_add_user_profile_data(self):
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

    def test_add_already_existed_email(self):
        mail = 'django@admin.ru'
        self.add_some_another_user(mail)

        response = self.client.post(self.url, data={'email': mail})
        self.assertContains(response, 'User with this email already exists.')

        response = self.client.get(self.url)
        self.assertNotContains(response, 'django@admin.ru')

    def test_add_incorrect_phone_number(self):
        response = self.client.post(self.url, data={'phone_number': '+7909298118'})
        self.assertContains(response, 'Enter a valid phone number')

        response = self.client.get(self.url)
        self.assertNotContains(response, '+7909298118')

    def test_add_phone_number_if_exists(self):
        username, _ = self.get_root_user()
        user = self.User.objects.get(username=username)

        user.profile.phone_number = "+79092981182"
        user.profile.save()

        response = self.client.post(self.url, data={'phone_number': '+79092981182'})
        self.assertContains(response, 'Phone number already exists')

        response = self.client.get(self.url)
        self.assertNotContains(response, '+79092981182')

    def test_change_phone_number_to_current(self):
        username, password = self.get_basic_user()

        user = self.User.objects.get(username=username)

        user.profile.phone_number = "+79092981182"
        user.profile.save()

        self.client.login(username=username, password=password)
        response = self.client.get(self.url)

        self.assertContains(response, "+79092981182")

        response = self.client.post(self.url, data={'phone_number': '+79092981182'})
        self.assertContains(response, 'Профиль успешно сохранен')

    def add_some_another_user(self, mail):
        self.User.objects.create(
            username='Test',
            password='12345',
            email=mail,
        )
