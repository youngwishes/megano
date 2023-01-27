from megano.core.loading import get_model

Category = get_model('catalog', 'Category')


class GlobalSettingsConfig:
    __instance = None

    def __new__(cls, *args, **kwargs):
        if cls.__instance is None:
            cls.__instance = super().__new__(cls)

        return cls.__instance

    def __init__(
            self, delivery_prices_difference, is_payment_available,
            categories, min_price_to_free_delivery, basic_delivery_price,
            promotions, reviews
    ):
        self.delivery_prices_difference: int = delivery_prices_difference
        self.is_payment_available: str = is_payment_available
        self.categories: list = categories
        self.min_price_to_free_delivery: int = min_price_to_free_delivery
        self.basic_delivery_price: int = basic_delivery_price
        self.promotions: list = promotions
        self.reviews: bool = reviews

    @property
    def delivery_prices_difference(self):
        return self._delivery_prices_difference

    @delivery_prices_difference.setter
    def delivery_prices_difference(self, delivery_prices_difference):
        self._delivery_prices_difference = delivery_prices_difference

    @property
    def is_payment_available(self):
        return self._is_payment_available

    @is_payment_available.setter
    def is_payment_available(self, is_payment_available):
        self._is_payment_available = is_payment_available

    @property
    def categories(self):
        return self._categories

    @categories.setter
    def categories(self, categories):
        if categories == "__all__":
            self._categories = Category.objects.all()
        else:
            self._categories = categories

    @property
    def min_price_to_free_delivery(self):
        return self._min_price_to_free_delivery

    @min_price_to_free_delivery.setter
    def min_price_to_free_delivery(self, min_price_to_free_delivery):
        self._min_price_to_free_delivery = min_price_to_free_delivery

    @property
    def basic_delivery_price(self):
        return self._basic_delivery_price

    @basic_delivery_price.setter
    def basic_delivery_price(self, basic_delivery_price):
        self._basic_delivery_price = basic_delivery_price

    @property
    def promotions(self):
        return self._promotions

    @promotions.setter
    def promotions(self, promotions):
        if promotions == "__all__":
            self._promotions = "__all__" # Доработаю когда сделаю нужные модели
        else:
            self._promotions = promotions

    @property
    def reviews(self):
        return self._reviews

    @reviews.setter
    def reviews(self, reviews):
        self._reviews = reviews

    def get_config(self):
        return {
            'delivery_prices_difference': self.delivery_prices_difference,
            'is_payment_available': self.is_payment_available,
            'categories': self.categories,
            'min_price_to_free_delivery': self.min_price_to_free_delivery,
            'basic_delivery_price': self.basic_delivery_price,
            'promotions': self.promotions,
            'reviews': self.reviews,
        }

    def set_config(self, user_config: dict):
        self.delivery_prices_difference: int = int(user_config['delivery_prices_difference'])
        self.is_payment_available: str = user_config['is_payment_available']
        self.categories: list = user_config['categories']
        self.min_price_to_free_delivery: int = int(user_config['min_price_to_free_delivery'])
        self.basic_delivery_price: int = int(user_config['basic_delivery_price'])
        self.promotions: list = user_config['promotions']
        self.reviews: str = user_config['reviews']


config = {
    "delivery_prices_difference": 500,
    "is_payment_available": "Y",
    "categories": "__all__",
    "min_price_to_free_delivery": 2000,
    "basic_delivery_price": 200,
    "promotions": "__all__",
    "reviews": "Y",
}

global_settings = GlobalSettingsConfig(**config)
