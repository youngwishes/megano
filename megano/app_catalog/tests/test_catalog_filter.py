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

            response = self.client.post(f"{reverse('catalog-search')}?s={slug}", data={'price': ['110;130']})

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
                f"{reverse('catalog-search')}?s={slug}", data={'price': ['110;130'], 'in_stock': True}
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

    def test_name_filter_contains(self):
        for category in self.Category.objects.all():
            slug = category.slug
            random_end = random.randint(1, 5)
            products = self.Product.objects.filter(categories__slug=slug).filter(name__iendswith=random_end)
            response = self.client.post(f"{reverse('catalog-search')}?s={slug}", data={'name': random_end})
            for p in products:
                self.assertContains(response, p)
