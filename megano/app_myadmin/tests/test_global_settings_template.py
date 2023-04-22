from django.test import TestCase
from django.urls import reverse
from megano.core.tests.mixins import TestInitialUserDataMixin


class TestGlobalSettingsTemplate(TestInitialUserDataMixin, TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.set_up_user_data()

    def test_global_settings_template_if_login_not_superuser(self):
        url = reverse('global_settings')
        username, password = self.get_basic_user()
        self.client.login(username=username, password=password)
        response = self.client.get(url)

        self.assertTemplateUsed(response, 'errors/403.html')

    def test_global_settings_view_if_login_superuser(self):
        url = reverse('global_settings')
        username, password = self.get_root_user()
        self.client.login(username=username, password=password)
        response = self.client.get(url)

        self.assertContains(response, "Глобальные настройки сайта")
        self.assertTemplateUsed(response, 'app_myadmin/admin_global_settings.html')
