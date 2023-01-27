from django.test import TestCase
from django.urls import reverse
from megano.core.tests.mixins import TestInitialUserDataMixin
from megano.core.loading import get_model
from bs4 import BeautifulSoup

Category = get_model('catalog', 'Category')


class TestGlobalSettingsViewAuth(TestInitialUserDataMixin, TestCase):
    def test_global_settings_view_not_login_user(self):
        url = reverse('global_settings')
        response = self.client.get(url)
        next_page = '?' + response.url.split('?')[1]

        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse('login') + next_page)

    def test_global_settings_view_if_login_not_superuser(self):
        url = reverse('global_settings')
        username, password = self.get_basic_user()
        self.client.login(username=username, password=password)
        response = self.client.get(url)
        self.assertEqual(response.status_code, 403)

    def test_global_settings_view_if_login_superuser(self):
        url = reverse('global_settings')
        username, password = self.get_root_user()
        self.client.login(username=username, password=password)
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)


class TestGlobalSettingsViewForm(TestInitialUserDataMixin, TestCase):

    def setUp(self) -> None:
        username, password = self.get_root_user()
        self.client.login(username=username, password=password)
        self.url = reverse('global_settings')
        self.data = {
            'delivery_prices_difference': 500,
            'is_payment_available': 'Y',
            'min_price_to_free_delivery': 2000,
            'basic_delivery_price': 200,
            'reviews': 'Y',
        }

    @classmethod
    def add_categories(cls):
        for i in range(5):
            cat = Category(name=f'Category {i + 1}')
            cat.save()

    def get_form_value(self, field_name, field_type, is_int):
        response = self.client.get(self.url)
        soup = BeautifulSoup(response.content, 'html.parser')

        form_value = soup.find(field_type, id=f'id_{field_name}')
        if field_type != 'input':
            for option in form_value:
                if "selected" in str(option):
                    form_value = option["value"]
                    break
        else:
            form_value = form_value['value']

        return int(form_value) if is_int else form_value

    def test_categories_checkboxes_if_not_categories(self):
        response = self.client.get(self.url)
        self.assertNotContains(response, 'Category 1')

    def test_categories_checkboxes_if_categories(self):
        self.add_categories()
        response = self.client.get(self.url)
        for i in range(5):
            self.assertContains(response, f'Category {i + 1}')

    def test_field_delivery_prices_difference(self):
        self.data['delivery_prices_difference'] = 5000
        old_value = self.get_form_value('delivery_prices_difference', field_type='input', is_int=True)

        self.client.post(self.url, data=self.data)
        new_value = self.get_form_value('delivery_prices_difference', field_type='input', is_int=True)

        self.assertNotEqual(old_value, new_value)
        self.assertEqual(old_value + 4500, new_value)

    def test_field_is_payment_available(self):
        old_value = self.get_form_value('is_payment_available', field_type='select', is_int=False)
        self.data['is_payment_available'] = 'N'
        self.client.post(self.url, data=self.data)
        new_value = self.get_form_value('is_payment_available', field_type='select', is_int=False)

        self.assertEqual(old_value, 'Y')
        self.assertEqual(new_value, 'N')

    def test_field_min_price_to_free_delivery(self):
        self.data['min_price_to_free_delivery'] = 3000
        old_value = self.get_form_value('min_price_to_free_delivery', field_type='input', is_int=True)

        self.client.post(self.url, data=self.data)
        new_value = self.get_form_value('min_price_to_free_delivery', field_type='input', is_int=True)

        self.assertNotEqual(old_value, new_value)
        self.assertEqual(old_value + 1000, new_value)

    def test_field_basic_delivery_price(self):
        self.data['basic_delivery_price'] = 500
        old_value = self.get_form_value('basic_delivery_price', field_type='input', is_int=True)

        self.client.post(self.url, data=self.data)
        new_value = self.get_form_value('basic_delivery_price', field_type='input', is_int=True)

        self.assertNotEqual(old_value, new_value)
        self.assertEqual(old_value + 300, new_value)

    def test_field_reviews(self):
        old_value = self.get_form_value('reviews', field_type='select', is_int=False)
        self.data['reviews'] = 'N'
        self.client.post(self.url, data=self.data)
        new_value = self.get_form_value('reviews', field_type='select', is_int=False)

        self.assertEqual(old_value, 'Y')
        self.assertEqual(new_value, 'N')
