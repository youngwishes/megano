from django.core.management import BaseCommand
from megano.core.loading import get_model

Product = get_model('product', 'Product')
ProductCommercial = get_model('product', 'ProductCommercial')


class Command(BaseCommand):
    def handle(self, *args, **options):
        for p in Product.objects.all():
            p.delete()

        for p in ProductCommercial.objects.all():
            p.delete()

        self.stdout.write(self.style.SUCCESS("Products has been successfully deleted"))
