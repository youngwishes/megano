from django.contrib import admin
from django.utils.safestring import mark_safe
from .inlines import *
from django_json_widget.widgets import JSONEditorWidget
from django.db.models import JSONField


class ProductTagAdmin(admin.ModelAdmin):
    list_display = ['id', 'name']
    fields = ('name',)


class ProductImageAdmin(admin.ModelAdmin):
    list_display = ['id', 'image', 'product']


class ProductAdmin(admin.ModelAdmin):
    list_display = ['id', 'name', 'short_description', 'get_html_photo']
    fields = ['name', 'description', 'short_description', 'specifications']
    formfield_overrides = {
        JSONField: {"widget": JSONEditorWidget}
    }

    inlines = [
        ProductCommercialInline,
        ProductImageInline,
        CategoriesInline,
        ProductTagInline,
    ]

    @admin.decorators.display(description="Photo")
    def get_html_photo(self, instance):
        if instance.images:
            return mark_safe(
                f"<a href='{instance.images.first().url}'>"
                f"<img src='{instance.images.first().url}' width=75>"
                f"</a>"
            )


admin.site.register(Product, ProductAdmin)
admin.site.register(ProductImage, ProductImageAdmin)
admin.site.register(ProductTag, ProductTagAdmin)
