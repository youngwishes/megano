from operator import ge
from django.shortcuts import render
from django.views import generic
from django.contrib.auth.views import LoginView, LogoutView


class RegisterView(generic.CreateView):
    pass


class LoginView(LoginView):
    pass


class LogoutView(LogoutView):
    pass
