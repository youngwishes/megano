from interfaces.services import Service

#Задача 12. Разработка заглушки сервиса добавления отзыва к товару

class AddNewReviewService(Service):
    def add_review(self, text):
        return text

    def get_reviews_from_product(self, product):
        return {
            'user_1': [
                'review_1',
                'review_2',
            ],
            'user_2': [
                'review_1',
                'review_2'
            ]
        }
    
    def get_reviews_count_from_product(self):
        return 20

    def get_sale_to_cart(self):
        return 200
    
    def execute(self, *args, **kwargs):
        pass