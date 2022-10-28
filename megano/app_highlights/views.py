from django.shortcuts import render
from django.views import View, generic

class HighLightsView(View):
    def get(self, request, *args, **kwargs):
        return render(request, 'app_highlights/sale.html')
