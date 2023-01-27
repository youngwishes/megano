from django.apps import AppConfig
from django.utils.translation import gettext_lazy as _


class AppCatalogConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'app_catalog'
    label = 'catalog'
    verbose_name = _("Catalog")
