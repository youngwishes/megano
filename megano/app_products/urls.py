from django.urls import path
from .views import *

urlpatterns = [
    path('<slug:slug>/', ProductDetailView.as_view(), name='product'),
]
