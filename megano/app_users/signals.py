from django.conf import settings
from django.contrib.auth import get_user_model
from django.db.models.signals import post_save
from django.dispatch import receiver
from megano.core.loading import get_model
from .services.role_manager import RoleManager

Profile = get_model('user', 'Profile')
Role = get_model('user', 'Role')
User = get_user_model()


@receiver(post_save, sender=settings.AUTH_USER_MODEL)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)
        instance.role = Role.objects.get(name=RoleManager(instance).get_user_role())
        instance.save()
