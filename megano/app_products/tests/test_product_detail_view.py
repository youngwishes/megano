import os
import random
from django.test import TestCase
from django.conf import settings

from megano.core.loading import get_model

Product = get_model('product', 'Product')
ProductCommercial = get_model('product', 'ProductCommercial')
ProductImage = get_model('product', 'ProductImage')
Category = get_model('catalog', 'Category')


class TestProductDetailView(TestCase):
    @classmethod
    def setUpTestData(cls):
        images_dir = os.path.join(settings.BASE_DIR, 'media', 'products')
        images = os.listdir(images_dir)

        for i in range(1, 3):
            random_img = random.choice(images)
            product = Product.objects.create(
                name=f'Название № {i}',
                description=f'Идеальный товар для вашего пользования № {i}',
                short_description=f'Короткое описание № {i}',
                specifications=[
                    {'Основные характеристики': {
                        'цвет': f'зелёный {i}',
                        'бренд': f'apple {i}',
                    }},
                    {'Технические характеристики': {
                        'экран': f'oled {i}',
                        'аккумулятор': f'аккум № {i} '
                    }}
                ],
            )

            product.images.create(image=random_img)

            ProductCommercial.objects.create(
                price=100,
                count=10,
                is_active=True,
                product=product,
            )

            product.save()

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
