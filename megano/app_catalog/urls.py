from django.urls import path
from .views import *

urlpatterns = [
    path('', CatalogView.as_view(), name='catalog'),
    path('search/', CatalogSearch.as_view(), name='catalog-search'),
]
