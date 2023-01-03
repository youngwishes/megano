from django.apps import AppConfig
from django.utils.translation import gettext_lazy as _


class AppUsersConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'app_users'
    label = 'user'
    verbose_name = _("Users")

    def ready(self):
        import app_users.signals
