from django.db.models import Q
from django.test import TestCase
from django.urls import reverse
from megano.core.loading import get_model
from megano.core.tests.mixins import TestInitialUserDataMixin

Category = get_model('catalog', 'Category')
Product = get_model('product', 'Product')
ProductCommercial = get_model('product', 'ProductCommercial')


class TestCatalogView(TestInitialUserDataMixin, TestCase):
    catalog_url = reverse('catalog')
    catalog_search_url = reverse('catalog-search')
    global_settings_params = {
        'delivery_prices_difference': 500,
        'is_payment_available': 'Y',
        'min_price_to_free_delivery': 2000,
        'basic_delivery_price': 200,
        'reviews': 'Y',
    }

    @classmethod
    def setUpTestData(cls):
        for i in range(1, 6):
            category = Category.objects.create(
                name=f'Category name {i}',
                image=b'',
                is_public=True,
            )

            product = category.products.create(
                name=f'Product {i}',
                description=f'Description {i}',
                short_description='',
                specifications={"colour": "blue"},
            )

            ProductCommercial.objects.create(
                price=100,
                count=10,
                is_active=True,
                product=product,
            )

            product.save()

        cls.set_up_user_data()

    def test_catalog_view_access(self):
        response = self.client.get(self.catalog_url)

        self.assertEqual(response.status_code, 200)

    def test_catalog_template_used(self):
        response = self.client.get(self.catalog_url)

        self.assertTemplateUsed(response, 'app_catalog/catalog_with_categories.html')

    def test_catalog_categories_contains(self):
        response = self.client.get(self.catalog_url)
        categories = Category.objects.all()

        for category in categories:
            self.assertContains(response, category)

    def test_catalog_search_view(self):
        response = self.client.get(self.catalog_search_url)
        self.assertEqual(response.status_code, 200)

    def test_catalog_search_template(self):
        response = self.client.get(self.catalog_search_url)
        self.assertTemplateUsed(response, 'app_catalog/catalog.html')

    def test_catalog_search_without_get_params(self):
        response = self.client.get(self.catalog_search_url)
        for i_product in Product.objects.all():
            self.assertNotContains(response, i_product)

    def test_catalog_search_with_get_params(self):
        for category in Category.objects.all():
            slug = category.slug

            response = self.client.get(self.catalog_search_url, data={'s': slug})
            product_that_must_contains = Product.objects.get(categories=category)
            products_not_contains = Product.objects.filter(~Q(categories=category))

            self.assertEqual(response.status_code, 200)
            self.assertTemplateUsed(response, 'app_catalog/catalog.html')
            self.assertContains(response, product_that_must_contains)

            for product in products_not_contains:
                self.assertNotContains(response, product)

    def test_if_categories_in_global_settings(self):
        username, password = self.get_root_user()

        self.client.login(username=username, password=password)

        global_settings_url = reverse('global_settings')

        response = self.client.get(global_settings_url)

        for category in Category.objects.all():
            self.assertContains(response, category)

    def test_global_filter_if_selected(self):
        username, password = self.get_root_user()
        self.client.login(username=username, password=password)

        global_settings_url = reverse('global_settings')
        self.global_settings_params['categories'] = Category.objects.values_list('id', flat=True)

        self.client.post(global_settings_url, data=self.global_settings_params)
        response = self.client.get(self.catalog_url)

        for category in Category.objects.all():
            self.assertContains(response, category)

    def test_global_filter_if_not_selected(self):
        username, password = self.get_root_user()
        self.client.login(username=username, password=password)

        global_settings_url = reverse('global_settings')
        self.global_settings_params['categories'] = Category.objects.none()

        self.client.post(global_settings_url, data=self.global_settings_params)

        prohibited_categories = Category.objects.all()
        response = self.client.get(self.catalog_url)

        for category in prohibited_categories:
            self.assertNotContains(response, category)
