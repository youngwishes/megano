"""megano URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.conf.urls import handler403, handler404
from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

handler403 = 'megano.core.views.csrf_failure'
handler404 = 'megano.core.views.page_not_found'

urlpatterns = [
    path('', include('app_root.urls')),
    path('', include('app_users.urls')),
    path('admin/global/', include('app_myadmin.urls')),
    path('admin/', admin.site.urls),
    path('highlight/', include('app_highlights.urls')),
    path('category/', include('app_catalog.urls')),
    path('cart', include('app_cart.urls')),
    path('product', include('app_products.urls')),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
