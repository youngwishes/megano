from django.shortcuts import render
from django.views import View, generic
from megano.core.loading import get_model

Category = get_model('catalog', 'Category')


class CatalogView(View):
    def get(self, request):
        categories = Category.objects.all()

        context = {
            "categories": categories
        }

        return render(request, 'app_catalog/catalog_with_categories.html', context)
        # return render(request, 'app_catalog/catalog.html')