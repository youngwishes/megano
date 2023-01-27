from django.shortcuts import render
from django.views import View, generic


class CartView(View):
    def get(self, request, *args, **kwargs):
        return render(request, 'app_cart/cart.html')


class PaymentView(View):
    def get(self, request, *args, **kwargs):
        return render(request, 'app_cart/payment.html')
