from django.contrib.auth import get_user_model
import os
import random
from django.conf import settings
from megano.core.loading import get_model

Product = get_model('product', 'Product')
ProductCommercial = get_model('product', 'ProductCommercial')
ProductImage = get_model('product', 'ProductImage')
Category = get_model('catalog', 'Category')
User = get_user_model()

ROOT_USERNAME = "root"
NOT_ROOT_USERNAME = "danil"


class TestInitialUserDataMixin:
    User = User

    @classmethod
    def set_up_user_data(cls):
        User.objects.create(
            username=ROOT_USERNAME,
            password="1234",
            is_superuser=True,
        )

        User.objects.create(
            username=NOT_ROOT_USERNAME,
            password="1234",

        )

    @classmethod
    def get_root_user(cls):
        root = User.objects.get(username=ROOT_USERNAME)
        new_password = User.objects.make_random_password()
        root.set_password(new_password)
        root.save()

        return root.username, new_password

    @classmethod
    def get_basic_user(cls):
        user = User.objects.get(username=NOT_ROOT_USERNAME)
        new_password = User.objects.make_random_password()

        user.set_password(new_password)
        user.save()
        return user.username, new_password


class TestProductsDataMixin:
    Category = Category
    Product = Product

    @classmethod
    def set_up_product_data(cls):
        images_dir = os.path.join(settings.BASE_DIR, 'media', 'products')
        images = os.listdir(images_dir)

        for i in range(1, 3):
            Category.objects.create(
                name=f'Category {i}',
                description=f'Category description {i}',
                image=b'',
                is_public=True,
            )

        categories = Category.objects.all()

        for i in range(1, 5):
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
                price=100 + i * 10,
                count=random.randint(0, 1),
                is_active=True,
                product=product,
            )

            product.categories.add(random.choice(categories))

            product.save()
