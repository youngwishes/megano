from django.db import models
from phonenumber_field.modelfields import PhoneNumberField
from django.utils.translation import gettext_lazy as _


class AbstractProfile(models.Model):
    user = models.OneToOneField('User', on_delete=models.CASCADE)
    phone_number = PhoneNumberField(blank=True, region="RU", max_length=12)
    bank_card = models.CharField(_("bank card number"), max_length=16, blank=True)

    class Meta:
        abstract = True
        verbose_name = _("Profile")
        verbose_name_plural = _("Profiles")
        ordering = ['user']
        app_label = "user"

    def __str__(self):
        return self.user.username


class AbstractRole(models.Model):

    CHOICES = (
        ("admin", "Administrator"),
        ("customer", "Customer"),
        ("anon", "Anonymous"),
    )

    name = models.CharField(_("role name"), choices=CHOICES, max_length=13, unique=True)

    def __str__(self):
        return self.name

    class Meta:
        abstract = True
        verbose_name = _("Role")
        verbose_name_plural = _("Roles")
        ordering = ['name']
        app_label = "user"
