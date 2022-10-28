from django.urls import path
from .views import *

urlpatterns = [
    path('', HighLightsView.as_view(), name='sale')
]