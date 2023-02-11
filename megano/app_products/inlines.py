from django.contrib.admin import TabularInline, StackedInline
from megano.core.loading import get_model

__all__ = [
    'ProductImageInline',
    'CategoriesInline',
    'ProductCommercialInline',
    'Product',
    'ProductCommercial',
    'ProductImage',
    'ProductTagInline',
    'ProductTag',
]

Product = get_model('product', 'Product')
ProductCommercial = get_model('product', 'ProductCommercial')
ProductImage = get_model('product', 'ProductImage')
ProductTag = get_model('product', 'ProductTag')


class ProductTagInline(TabularInline):
    model = Product.tags.through
    verbose_name = "product tag"
    verbose_name_plural = "product tags"


class ProductImageInline(TabularInline):
    model = ProductImage


class CategoriesInline(TabularInline):
    model = Product.categories.through


class ProductCommercialInline(StackedInline):
    model = ProductCommercial
    fields = ['price', 'count', 'is_active', 'product', 'highlights']
    filter_horizontal = ("highlights",)
