from django.shortcuts import render
from django.views import View, generic


class CatalogView(View):
    def get(self, request, *args, **kwargs):
        return render(request, 'app_catalog/catalog.html')