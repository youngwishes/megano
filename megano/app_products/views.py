from django.shortcuts import render
from django.views import View, generic
from django.views.generic import DetailView
from megano.core.loading import get_model

ProductCommercial = get_model("product", "ProductCommercial")
ProductImage = get_model('product', 'ProductImage')
Product = get_model('product', 'Product')


class ProductDetailView(DetailView):
    template_name = "app_products/product.html"
    model = Product
    context_object_name = "product"
    slug_url_kwarg = "slug"
    slug_field = "vendor_code"

