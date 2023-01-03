from django.apps import AppConfig
from django.utils.translation import gettext_lazy as _


class AppProductsConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'app_products'
    label = "product"
    verbose_name = _("Product")


