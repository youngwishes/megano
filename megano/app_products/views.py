from django.shortcuts import render
from django.views import View, generic
from django.views.generic import DetailView
from megano.core.loading import get_model

ProductCommercial = get_model("product", "ProductCommercial")
ProductImage = get_model('product', 'ProductImage')


class ProductDetailView(DetailView):
    template_name = "app_products/product.html"
    model = ProductCommercial
    context_object_name = "commercial_product"
    slug_url_kwarg = "vendor_code"
    slug_field = "vendor_code"

    def get_context_data(self, **kwargs):
        context = super().get_context_data()
        context['images'] = ProductImage.objects.filter(product=self.object.product)
        context['specifications'] = self.object.product.specifications

        return context
