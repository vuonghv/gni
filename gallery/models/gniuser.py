from django.conf import settings
from django.db import models
from django.contrib.auth.models import User

from gallery.models.image import Image


def upload_to_dir(instance, filename):
    return '{user_id}/{dirname}/{filename}'.format(
                        user_id=instance.user.id,
                        dirname=settings.AVATAR_DIR_NAME,
                        filename=filename)


class GNIUser(models.Model):
    """
    GNI's User model associated with the User model of django
    """
    avatar = models.ImageField(
                        null=True, upload_to=upload_to_dir, max_length=257)
    twitter = models.CharField(max_length=257, blank=True, default='')

    user = models.OneToOneField(User)
