from django.db import models
from django.contrib.auth.models import User

from .image import Image


class Comment(models.Model):
    content = models.TextField(null=False, blank=False)
    time_updated = models.DateTimeField(auto_now=True)

    owner = models.ForeignKey(User, related_name='comments')

    users_like = models.ManyToManyField(User, related_name='liked_comments')

    image = models.ForeignKey(Image, related_name='comments')

    def __str__(self):
        return self.content
