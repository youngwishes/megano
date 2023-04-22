import random
from django.test import TestCase
from megano.core.tests.mixins import TestProductsDataMixin
from django.urls import reverse


class TestCatalogFilter(TestProductsDataMixin, TestCase):

    @classmethod
    def setUpTestData(cls):
        cls.set_up_product_data()

    def test_range_price_filter(self):
        for category in self.Category.objects.all():
            slug = category.slug
            products = self.Product.objects.filter(categories__slug=slug).filter(commercial__price__range=[110, 130])

            response = self.client.post(f"{reverse('catalog-search')}?s={slug}", data={'price': '110;130'})

            for p in products:
                self.assertContains(response, p)

    def test_in_stock_filter(self):
        for category in self.Category.objects.all():
            slug = category.slug
            products = self.Product.objects.filter(categories__slug=slug).filter(commercial__count__gt=0)
            response = self.client.post(f"{reverse('catalog-search')}?s={slug}", data={'in_stock': True})
            for p in products:
                self.assertContains(response, p)

    def test_in_stock_and_price_range_filter(self):
        for category in self.Category.objects.all():
            slug = category.slug
            products = self.Product.objects.filter(categories__slug=slug) \
                .filter(commercial__price__range=[110, 130]) \
                .filter(commercial__count__gt=0)

            response = self.client.post(
                f"{reverse('catalog-search')}?s={slug}", data={'price': '110;130', 'in_stock': True}
            )

            for p in products:
                self.assertContains(response, p)

    def test_name_filter_startswith(self):
        for category in self.Category.objects.all():
            slug = category.slug
            products = self.Product.objects.filter(categories__slug=slug).filter(name__istartswith="Наз")
            response = self.client.post(f"{reverse('catalog-search')}?s={slug}", data={'name': 'Наз'})
            for p in products:
                self.assertContains(response, p)

    def test_name_filter_endswith(self):
        for category in self.Category.objects.all():
            slug = category.slug
            random_end = random.randint(1, 5)
            products = self.Product.objects.filter(categories__slug=slug).filter(name__iendswith=random_end)
            response = self.client.post(f"{reverse('catalog-search')}?s={slug}", data={'name': random_end})

            for p in products:
                self.assertContains(response, p)

    def test_name_filter_contains_if_len_gt_3(self):
        part_of_product_name = "азв"

        for category in self.Category.objects.all():
            slug = category.slug
            products = self.Product.objects.filter(categories__slug=slug).filter(name__icontains=part_of_product_name)
            response = self.client.post(f"{reverse('catalog-search')}?s={slug}", data={'name': part_of_product_name})
            for p in products:
                self.assertContains(response, p)

    def test_name_filter_contains_if_len_lt_3(self):
        part_of_product_name = "аз"

        for category in self.Category.objects.all():
            slug = category.slug
            products = self.Product.objects.filter(categories__slug=slug).filter(name__icontains=part_of_product_name)
            response = self.client.post(f"{reverse('catalog-search')}?s={slug}", data={'name': part_of_product_name})
            for p in products:
                self.assertNotContains(response, p)

    def test_price_range_in_stock_name_filtering(self):

        params = {
            'name': 'Назв',
            'price': '100;120',
            'in_stock': True,
        }

        for category in self.Category.objects.all():
            slug = category.slug
            products = self.Product.objects.filter(categories__slug=slug)

            products_have_to_be = products.filter(name__istartswith='Назв',
                                                  commercial__price__range=(100, 120),
                                                  commercial__count=1)

            products_have_not_to_be = products.filter(commercial__price__range=(130, 140)) | \
                                      products.filter(commercial__count=0)

            response = self.client.post(f'{reverse("catalog-search")}?s={slug}', data=params)

            for p in products_have_to_be:
                self.assertTrue(p.commercial.price in range(100, 121))
                self.assertTrue(p.commercial.count == 1)
                self.assertTrue(p.name.startswith('Назв'))
                self.assertContains(response, p)

            for p in products_have_not_to_be:

                is_product = p.commercial.price in range(130, 141) or \
                             p.commercial.count == 0 or \
                             p.name.startswith('Прод')

                self.assertTrue(is_product)
                self.assertNotContains(response, p)
