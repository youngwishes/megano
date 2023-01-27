from django.contrib.auth.mixins import UserPassesTestMixin
from django.shortcuts import render
from django.views import View
from .forms import GlobalSettingsForm
from megano.core.config import global_settings
from megano.core.loading import get_model


Category = get_model('catalog', 'Category')


class GlobalSiteSettings(UserPassesTestMixin, View):

    def test_func(self):
        return self.request.user.is_superuser

    def get(self, request):
        form = GlobalSettingsForm(initial=global_settings.get_config())
        context = {
            "form": form
        }

        return render(request, 'app_myadmin/admin_global_settings.html', context)

    def post(self, request):
        form = GlobalSettingsForm(request.POST)

        if form.is_valid():
            global_settings.set_config(form.cleaned_data)
        else:
            print(form.errors)


        context = {
            "form": form
        }

        return render(request, 'app_myadmin/admin_global_settings.html', context)
