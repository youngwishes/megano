from django.contrib.auth import get_user_model, authenticate
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django import forms
from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _
from megano.core.loading import get_model
from django.contrib.auth.forms import PasswordChangeForm

User = get_user_model()
Profile = get_model('user', 'Profile')


class ExtendedUserCreationForm(UserCreationForm):
    password1 = forms.CharField(widget=forms.PasswordInput(
        attrs={
            "class": "form-input",
            "id": "id_password1",
            "name": "password1"
        }
    ), label=_("Password"))

    password2 = forms.CharField(widget=forms.PasswordInput(
        attrs={
            "class": "form-input",
            "id": "id_password2",
            "name": "password2",
        }
    ), label=_("Confirm password"))

    class Meta:
        fields = ("username", "email", "first_name", "last_name")
        model = User
        widgets = {
            'email': forms.EmailInput(attrs={"class": "form-input", "id": "id_email", "name": "email"}),
            'username': forms.TextInput(attrs={"class": "form-input", "id": "id_username", "name": "username"}),
            'first_name': forms.TextInput(attrs={"class": "form-input", "id": "id_first_name", "name": "first_name"}),
            'last_name': forms.TextInput(attrs={"class": "form-input", "id": "id_last_name", "name": "last_name"}),

        }
        labels = {
            "email": _("E-mail")
        }

    def clean_email(self):
        email = self.cleaned_data['email']
        new = User.objects.filter(email=email)
        if new.count():
            raise ValidationError("Email already exist")
        return email


class UserLoginForm(AuthenticationForm):
    username = forms.CharField(
        widget=forms.TextInput(
            attrs={
                "class": "form-input",
                "id": "username",
                "name": "username",
            }
        ),
        label=_("Username or e-mail")
    )
    password = forms.CharField(
        widget=forms.PasswordInput(
            attrs={
                "class": "form-input",
                "id": "password",
                "name": "password",
            }
        ),
        label=_("Password"))

    error_messages = {
        "invalid_login": _(
            "Please enter a correct %(username)s and password. Note that both "
            "fields are case-sensitive."
        ),
        "inactive": _("This account is inactive."),
    }

    def clean(self):
        username_or_email = self.cleaned_data.get("username")
        password = self.cleaned_data.get("password")

        if username_or_email is not None and password:
            if User.objects.filter(email=username_or_email).exists():
                user = User.objects.get(email=username_or_email)
                self.user_cache = authenticate(
                    self.request, username=user.username, password=password
                )
            else:
                self.user_cache = authenticate(
                    self.request, username=username_or_email, password=password
                )

            if self.user_cache is None:
                raise self.get_invalid_login_error()
            else:
                self.confirm_login_allowed(self.user_cache)

        return self.cleaned_data


class ProfileForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ("phone_number", "avatar", "bank_card")
        widgets = {
            'phone_number': forms.TextInput(attrs={"class": "form-input", "id": "phone", "name": "phone"}),
            'bank_card': forms.TextInput(attrs={"class": "form-input", "id": "card", "name": "card"}),
            'avatar': forms.FileInput(attrs={"class": "Profile-file form-input", "id": "avatar", "name": "avatar"})
        }
        labels = {
            'phone_number': _('Phone number'),
            'bank_card': _('Bank card number'),
            'avatar': _('Avatar')
        }

    def clean_phone_number(self):
        phone_number = self.cleaned_data['phone_number']
        profiles = Profile.objects.filter(phone_number=phone_number)
        if not profiles.exists():
            return phone_number
        elif profiles.count() == 1:
            if self.instance == profiles[0]:
                return phone_number
        raise ValidationError("Phone number already exists")


class UserProfileForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ("first_name", 'last_name', 'email')
        widgets = {
            'first_name': forms.TextInput(attrs={"class": "form-input", "id": "first_name", "name": "first_name"}),
            'last_name': forms.TextInput(attrs={"class": "form-input", "id": "last_name", "name": "last_name"}),
            'email': forms.TextInput(attrs={"class": "form-input", "id": "mail", "name": "mail"})
        }
        labels = {
            'first_name': _('First name'),
            'last_name': _('Last name'),
            'email': _('E-mail')
        }

    def clean_email(self):
        if 'email' in self.changed_data:
            email = self.cleaned_data['email']
            if User.objects.filter(email=email).exists():
                raise ValidationError(_("User with this email already exists."), code='invalid')
            return email


class CustomPasswordChangeForm(PasswordChangeForm):
    old_password = forms.CharField(widget=forms.PasswordInput(
        attrs={
            "class": "form-input",
            "autocomplete": "new-password",
        }
    ), label=_("Old password"))

    new_password1 = forms.CharField(widget=forms.PasswordInput(
        attrs={
            "class": "form-input"
        }
    ), label=_("Password"))

    new_password2 = forms.CharField(widget=forms.PasswordInput(
        attrs={
            "class": "form-input"
        }
    ), label=_("Confirm password"))
