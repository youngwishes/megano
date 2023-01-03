from megano.core.loading import is_model_registered
from .abstract_models import *
from django.contrib.auth.models import AbstractUser
from django.utils.translation import gettext_lazy as _


__all__ = []

if not is_model_registered('user', 'Role'):
    class Role(AbstractRole):
        pass


    __all__.append("Role")

if not is_model_registered('user', 'User'):
    class User(AbstractUser):
        role = models.ForeignKey('user.Role', on_delete=models.PROTECT, null=True)


    __all__.append("User")

if not is_model_registered('user', 'Profile'):

    def user_media_path(instance, filename):
        return 'users/{username}/avatars/{filename}'.format(
            username=instance,
            filename=filename,
        )

    class Profile(AbstractProfile):
        avatar = models.FileField(_('profile photo'), upload_to=user_media_path, blank=True, default="users/default.png")


    __all__.append("Profile")
