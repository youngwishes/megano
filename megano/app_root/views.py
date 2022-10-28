from django.shortcuts import render
from django.views import generic, View


class MainPageView(View):
    def get(self, request, *args, **kwargs):
        return render(request, 'app_root/index.html')
