from django.contrib.admin import TabularInline, StackedInline
from megano.core.loading import get_model

__all__ = [
    'ProductImageInline',
    'CategoriesInline',
    'ProductCommercialInline',
    'Product',
    'ProductCommercial',
    'ProductImage'
]

Product = get_model('product', 'Product')
ProductCommercial = get_model('product', 'ProductCommercial')
ProductImage = get_model('product', 'ProductImage')


class ProductImageInline(TabularInline):
    model = ProductImage


class CategoriesInline(TabularInline):
    model = Product.categories.through


class ProductCommercialInline(StackedInline):
    model = ProductCommercial
    fields = ['price', 'count', 'is_active', 'product', 'highlights']
    filter_horizontal = ("highlights", )
