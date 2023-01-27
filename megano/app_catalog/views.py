from django.shortcuts import render
from django.views import View, generic
from megano.core.loading import get_model
from megano.core.config import global_settings

Category = get_model('catalog', 'Category')
Product = get_model('product', 'Product')


class CatalogView(View):
    def get(self, request):
        categories = Category.objects.filter(id__in=global_settings.categories)

        context = {
            "categories": categories
        }

        return render(request, 'app_catalog/catalog_with_categories.html', context)


class CatalogSearch(View):
    def get(self, request):
        get_data = request.GET.get('s')

        if get_data:
            products = Product.objects.filter(categories__slug=get_data)
        else:
            products = []

        context = {
            'products': products
        }

        return render(request, 'app_catalog/catalog.html', context)
