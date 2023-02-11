from django.apps import apps as django_apps
from django.core.exceptions import AppRegistryNotReady
from importlib import import_module
from django.apps.config import MODELS_MODULE_NAME


def is_model_registered(app_label, model_name):
    try:
        django_apps.get_registered_model(app_label, model_name)
    except LookupError:
        return False
    else:
        return True


def get_model(app_label, model_name):
    try:
        return django_apps.get_model(app_label, model_name)
    except AppRegistryNotReady:
        if django_apps.apps_ready and django_apps.models_ready:
            app_config = django_apps.get_app_config(app_label)
            print(app_config)
            import_module('%s.%s' % (app_config.name, MODELS_MODULE_NAME))
            return django_apps.get_registered_model(app_label, model_name)
        else:
            raise
