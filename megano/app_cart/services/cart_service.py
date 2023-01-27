from interfaces.services import Service

# Задача 11. Разработка заглушки сервиса добавления товара в корзину
class CartManager(Service):
    def add_product_to_user_cart(self, product):
        return True

    def remove_product_from_cart(self, product):
        return True

    def increase_product_count(self, product, amount):
        return self.get_count_of_product_in_cart(product) + amount

    def decrease_product_count(self, product, amount):
        return self.get_count_of_product_in_cart(product) - amount

    def get_products_cart(self):
        return {
            'category_1': {
                'item_1': 2,
                'item_2': 3,
            },

            'category_2': {
                'item_3': 4,
                'item_4': 5,
            }
        }

    def get_count_of_product_in_cart(self, product):
        return 10

    def get_count_of_products_in_cart(self):
        return 100

    def check_if_product_in_user_cart(self, product):
        return True

    def execute(self, *args, **kwargs):
        pass
