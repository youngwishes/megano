from django.urls import path
from .views import *

urlpatterns = [
    path('<slug:vendor_code>/', ProductDetailView.as_view(), name='product'),
]
