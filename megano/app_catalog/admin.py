from django.contrib import admin
from django.utils.safestring import mark_safe

from megano.core.loading import get_model

Category = get_model('catalog', 'Category')
CategoryCommercial = get_model('catalog', 'CategoryCommercial')


class CategoryAdmin(admin.ModelAdmin):
    list_display = ['id', 'name', 'is_public', 'get_html_photo']
    fields = ['name', 'image', 'is_public']
    readonly_fields = ("get_html_photo",)

    @admin.decorators.display(description="Photo")
    def get_html_photo(self, instance):
        if instance.image:
            return mark_safe(
                f"<a href='{instance.image.url}'><img src='{instance.image.url}' width=100></a>"
            )


class CategoryCommercialAdmin(admin.ModelAdmin):
    list_display = ['id', 'name', 'description', 'is_active']
    fields = ['name', 'description', 'is_active', 'valid_from', 'valid_to', 'discount']


admin.site.register(Category, CategoryAdmin)
admin.site.register(CategoryCommercial, CategoryCommercialAdmin)
