from django.contrib.auth import authenticate, login, get_user_model
from django.contrib.auth.forms import PasswordResetForm
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render, redirect
from django.views import generic, View
from django.contrib.auth.views import LoginView, LogoutView
from .forms import ExtendedUserCreationForm, UserLoginForm, UserProfileForm, ProfileForm, CustomPasswordChangeForm
from django.urls import reverse_lazy
from .services.password_reset_service import PasswordResetService
from megano.core.loading import get_model
from django.contrib.auth.views import PasswordChangeView as ChangePasswordView

User = get_user_model()
Role = get_model('user', 'Role')


class PasswordChangeView(ChangePasswordView):
    form_class = CustomPasswordChangeForm
    template_name = "app_users/password_change_form.html"
    success_url = reverse_lazy("password_change_done")


class RegisterView(generic.CreateView):
    template_name = "app_users/register.html"
    form_class = ExtendedUserCreationForm
    success_url = reverse_lazy('profile')

    def form_valid(self, form):
        result = super(RegisterView, self).form_valid(form)
        username = form.cleaned_data.get("username")
        password = form.cleaned_data.get("password1")
        user = authenticate(username=username, password=password)
        login(request=self.request, user=user)

        return result


class UserLoginView(LoginView):
    template_name = "app_users/login.html"
    redirect_authenticated_user = reverse_lazy("profile")
    authentication_form = UserLoginForm
    next_page = reverse_lazy("profile")


class UserLogoutView(LogoutView):
    next_page = "/"


class ProfileView(LoginRequiredMixin, View):
    def get(self, request):
        user, profile, avatar = self.get_account_info(request)

        profile_form = ProfileForm(instance=profile)
        user_form = UserProfileForm(instance=user)

        context = {
            "profile_form": profile_form,
            "user_form": user_form,
            "avatar": avatar
        }

        return render(request, 'app_users/profile.html', context)

    def post(self, request):
        user, profile, avatar = self.get_account_info(request)

        profile_form = ProfileForm(request.POST, request.FILES, instance=profile)
        user_form = UserProfileForm(request.POST, instance=user)

        context = {
            "profile_form": profile_form,
            "user_form": user_form,
            "avatar": avatar,
        }

        is_valid = all([user_form.is_valid(), profile_form.is_valid()])
        if is_valid:
            profile_form.save() and user_form.save()

        return render(request, "app_users/profile.html", context)

    @classmethod
    def get_account_info(cls, request):
        user = request.user
        profile = user.profile
        avatar = profile.avatar

        return user, profile, avatar


class PasswordResetView(View):
    def get(self, request):
        context = {
            "form": PasswordResetForm()
        }
        return render(request, 'app_users/password_reset_form.html', context)

    def post(self, request):
        password_reset_form = PasswordResetForm(request.POST)
        context = {"form": password_reset_form}

        if password_reset_form.is_valid():
            mail = password_reset_form.cleaned_data["email"]

            if PasswordResetService(email=mail).execute():
                return redirect("password_reset_done")
            else:
                password_reset_form.add_error(field="email", error="Invalid email address.")

        return render(request, 'app_users/password_reset_form.html', context)
