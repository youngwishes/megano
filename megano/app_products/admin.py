from django.contrib import admin
from megano.core.loading import get_model

Product = get_model('product', 'Product')
ProductCommercial = get_model('product', 'ProductCommercial')


class ProductAdmin(admin.ModelAdmin):
    list_display = ['id', 'name', 'short_description',]
    fields = ['name', 'description', 'short_description',]


class ProductCommercialAdmin(admin.ModelAdmin):
    list_display = ['vendor_code', 'price', 'count', 'is_active', 'product']
    fields = ['price', 'count', 'is_active']


admin.site.register(Product, ProductAdmin)
admin.site.register(ProductCommercial, ProductCommercialAdmin)
