from django.contrib.auth.views import (
    PasswordResetConfirmView,
    PasswordResetDoneView,
    PasswordResetCompleteView,
    PasswordChangeDoneView,
)

from django.urls import path
from .views import *

urlpatterns = [
    path('login/', UserLoginView.as_view(), name="login"),
    path('logout/', UserLogoutView.as_view(), name="logout"),
    path('register/', RegisterView.as_view(), name="register"),
    path('profile/', ProfileView.as_view(), name="profile"),
    path('password-reset/', PasswordResetView.as_view(), name="password_reset"),

    path('reset/<uidb64>/<token>/', PasswordResetConfirmView.as_view(
        template_name="app_users/password_reset_confirm.html"
    ), name="password_reset_confirm"),

    path('password-reset/done/', PasswordResetDoneView.as_view(
        template_name="app_users/password_reset_done.html",
    ), name="password_reset_done"),

    path('reset/done', PasswordResetCompleteView.as_view(
        template_name="app_users/password_reset_complete.html"
    ), name="password_reset_complete"),

    path('password-change/', PasswordChangeView.as_view(), name='password_change'),

    path('password-change/done/', PasswordChangeDoneView.as_view(
        template_name="app_users/password_change_done.html"
    ), name='password_change_done'),

]
