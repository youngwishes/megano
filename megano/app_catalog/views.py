from django.shortcuts import render
from django.views import View, generic
from megano.core.loading import get_model
from megano.core.config import global_settings

Category = get_model('catalog', 'Category')
ProductCommercial = get_model('product', 'ProductCommercial')


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
            commercial_products = ProductCommercial.objects.filter(product__categories__slug=get_data)
        else:
            commercial_products = []

        context = {
            'commercial_products': commercial_products
        }

        return render(request, 'app_catalog/catalog.html', context)
