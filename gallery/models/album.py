from django.db import models
from django.contrib.auth.models import User

from gallery.models.image import Image


class Album(models.Model):
    title = models.TextField(blank=True, default='')
    description = models.TextField(blank=True, default='')
    time_created = models.DateTimeField(auto_now_add=True)
    time_updated = models.DateTimeField(auto_now=True)

    thumbnail = models.ForeignKey(Image, null=True, default=None, related_name='+')

    owner = models.ForeignKey(User, related_name='albums')

    users_like = models.ManyToManyField(User, related_name='liked_albums')

    def __str__(self):
        return self.title

    def thumbnail_url(self):
        if self.thumbnail:
            return self.thumbnail.img.url
        elif self.images.all():
            return self.images.order_by('-time_created')[0].img.url

        return ''
