from django.urls import path
from .views import *

urlpatterns = [
    path('settings/', GlobalSiteSettings.as_view(), name="global_settings"),
]
