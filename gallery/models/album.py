from django.db import models
from django.contrib.auth.models import User


class Album(models.Model):
    title = models.TextField(blank=True, default='')
    description = models.TextField(blank=True, default='')
    time_created = models.DateTimeField(auto_now_add=True)
    time_updated = models.DateTimeField(auto_now=True)

    thumbnail = models.FilePathField(default='')

    owner = models.ForeignKey(User, related_name='albums')

    users_like = models.ManyToManyField(User, related_name='liked_albums')

    def __str__(self):
        return self.title
