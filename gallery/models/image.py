import hashlib

from django.utils import timezone
from django.db import models
from django.contrib.auth.models import User


def upload_to_dir(instance, filename):
    return '{user_id}/{album_id}/{filename}'.format(
                        user_id=instance.owner.id,
                        album_id=instance.album.id,
                        filename=filename)


class Image(models.Model):
    img = models.ImageField(upload_to=upload_to_dir, max_length=257)

    title = models.TextField(blank=True, default='')
    description = models.TextField(blank=True, default='')
    time_created = models.DateTimeField(auto_now_add=True)
    time_updated = models.DateTimeField(auto_now=True)

    album = models.ForeignKey('gallery.Album', related_name='images')

    owner = models.ForeignKey(User, related_name='images')

    users_like = models.ManyToManyField(User, related_name='liked_images')

    def __str__(self):
        return self.title
