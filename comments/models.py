from django.db import models
from django.conf import settings


class Comment(models.Model):
    content = models.TextField(null=False, blank=False)
    time_updated = models.DateTimeField(auto_now=True)

    owner = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='comments')

    users_like = models.ManyToManyField(settings.AUTH_USER_MODEL, related_name='liked_comments')

    image = models.ForeignKey('images.Image', related_name='comments')

    def __str__(self):
        return self.content
