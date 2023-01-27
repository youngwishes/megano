from django.urls import path
from .views import *

urlpatterns = [
    path('<slug:product_slug>/', ProductView.as_view(), name='product'),
]