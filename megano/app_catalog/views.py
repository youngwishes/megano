from django.shortcuts import render
from django.views import View
from megano.core.loading import get_model
from megano.core.config import global_settings
from megano.core.utils import get_cleaned_data_from_post_data
from django.core.cache import cache

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
        if category_slug == cache.get('cat_slug'):
            products = cache.get('filtered_products') or \
                       cache.get('products') or \
                       Product.objects.filter(categories__slug=category_slug)
        else:
            products = Product.objects.filter(categories__slug=category_slug)
            cache.set('cat_slug', category_slug)
            cache.set('products', products)
        context = {
            'products': products,
            'name': cache.get('name'),
            'price_from': cache.get('price_from'),
            'price_to': cache.get('price_to'),
            'in_stock': cache.get('in_stock'),
        }
        return render(request, 'app_catalog/catalog.html', context)

    def post(self, request):
        cleaned_data = get_cleaned_data_from_post_data(request.POST)
        category_slug = request.GET.get('s')
        if category_slug == cache.get('cat_slug'):
            products = cache.get('products').catalog_filter(cleaned_data)
        else:
            products = Product.objects.filter(categories__slug=category_slug).catalog_filter(cleaned_data)
        cache.set('filtered_products', products)
        context = {
            'products': products,
            'name': cache.get('name'),
            'price_from': cache.get('price_from'),
            'price_to': cache.get('price_to'),
            'in_stock': cache.get('in_stock'),
        }
        return render(request, 'app_catalog/catalog.html', context)
