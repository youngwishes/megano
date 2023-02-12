from django.db.models import Q
from django.shortcuts import render
from django.views import View
from megano.core.loading import get_model
from megano.core.config import global_settings
from megano.core.utils import get_cleaned_data_from_post_data

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
        category_slug = request.GET.get('s')
        if category_slug:
            products = Product.objects.filter(categories__slug=category_slug)
        else:
            products = []

        context = {
            'products': products
        }

        return render(request, 'app_catalog/catalog.html', context)

    def post(self, request):
        category_slug = request.GET.get('s')

        print(request.POST)

        cleaned_data = get_cleaned_data_from_post_data(request.POST)
        products = Product.objects.filter(categories__slug=category_slug).catalog_filter(cleaned_data)

        if cleaned_data.get('price_range'):
            price_from = cleaned_data.get('price_range').get('price_from')
            price_to = cleaned_data.get('price_range').get('price_to')
        else:
            price_from = 100
            price_to = 500_000

        in_stock = cleaned_data.get('in_stock')
        name = cleaned_data.get('name')

        context = {
            'products': products,
            'name': name,
            'price_from': price_from,
            'in_stock': in_stock,
            'price_to': price_to,
        }

        return render(request, 'app_catalog/catalog.html', context)
