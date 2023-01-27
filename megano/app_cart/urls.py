from django.urls import path
from .views import *

urlpatterns = [
    path('', CartView.as_view(), name='cart'),
    path('checkout/', PaymentView.as_view(), name='checkout'),
]
