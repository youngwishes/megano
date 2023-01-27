from django.contrib.auth import get_user_model
from django.contrib.auth.tokens import default_token_generator
from django.core.exceptions import ObjectDoesNotExist
from django.core.mail import send_mail, BadHeaderError
from django.http import HttpResponse
from django.template.loader import render_to_string
from django.utils.encoding import force_bytes
from django.utils.http import urlsafe_base64_encode

User = get_user_model()


class PasswordResetService:
    def __init__(self, email):
        self.email = email

    def _prepare_init_message_data(self, user):
        context = {
            "email": self.email,
            "domain": "127.0.0.1:8000",
            "site_name": "Megano",
            "uid": urlsafe_base64_encode(force_bytes(user.pk)),
            "user": user,
            "token": default_token_generator.make_token(user),
            "protocol": "http"
        }

        msg_html = render_to_string("app_users/password_reset_email.html", context)

        data = {
            "subject": "Reset password",
            "msg_html": msg_html,
        }

        return data

    def _find_user_by_email(self):
        try:
            user = User.objects.get(email=self.email)
        except ObjectDoesNotExist:
            return False
        else:
            return user

    def _send_mail_conf(self):
        user = self._find_user_by_email()
        if user:
            return self._prepare_init_message_data(user)
        else:
            return False

    def execute(self):
        data = self._send_mail_conf()

        if data:
            try:
                send_mail(subject=data.get("subject"),
                          from_email='megano.django@yandex.ru',
                          message="",
                          recipient_list=[self.email],
                          fail_silently=False,
                          html_message=data.get("msg_html"))
            except BadHeaderError:
                return HttpResponse('Недопустимый заголовок')
            else:
                return True
        else:
            return False
