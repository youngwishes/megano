from django.shortcuts import render
from django.views import View, generic


class ProductView(View):
    def get(self, request, *args, **kwargs):
        return render(request, 'app_products/product.html')
