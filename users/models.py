from django.db import models
from django.conf import settings
from django.contrib.auth.models import User


def _path_to_avatar(instance, filename):
    return '{user_id}/{dirname}/{filename}'.format(
                        user_id=instance.user.id,
                        dirname=settings.AVATAR_DIR_NAME,
                        filename=filename)


class UserProfile(models.Model):
    """
    User's profile adding more information for Django Auth User
    """
    user = models.OneToOneField(settings.AUTH_USER_MODEL, primary_key=True, related_name='profile')

    avatar = models.ImageField(upload_to=_path_to_avatar, blank=True, default='', max_length=257)
    twitter = models.CharField(max_length=256, blank=True, default='')
