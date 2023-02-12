from django.test import TestCase
from megano.core.loading import get_model
from megano.core.tests.mixins import TestProductsDataMixin


Product = get_model('product', 'Product')
ProductCommercial = get_model('product', 'ProductCommercial')
ProductImage = get_model('product', 'ProductImage')
Category = get_model('catalog', 'Category')


class TestProductDetailView(TestProductsDataMixin, TestCase):

    def test_status_code_is_200(self):
        for p in Product.objects.all():
            response = self.client.get(p.get_absolute_url())
            self.assertEqual(response.status_code, 200)
            self.assertTemplateUsed(response, 'app_products/product.html')

    def test_product_info_contains(self):
        for p in Product.objects.all():
            response = self.client.get(p.get_absolute_url())
            self.assertContains(response, p.name)
            self.assertContains(response, p.images.first().image)
            self.assertContains(response, p.description)
            self.assertContains(response, p.short_description)

            for spec in p.specifications:
                if isinstance(spec, dict):
                    for key, value in spec.items():
                        if isinstance(value, dict):
                            for k, v in value.items():
                                self.assertContains(response, k)
                                self.assertContains(response, v)
                        else:
                            self.assertContains(response, key)
                            self.assertContains(response, value)
                else:
                    self.assertContains(response, spec)
