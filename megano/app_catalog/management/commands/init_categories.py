from django.core.management import BaseCommand
from megano.core.loading import get_model

Category = get_model('catalog', 'Category')


class Command(BaseCommand):
    def handle(self, *args, **options):
        pass
