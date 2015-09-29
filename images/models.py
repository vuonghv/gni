from django.db import models
from django.conf import settings


def _path_to_file(instance, filename):
    return '{user_id}/{album_id}/{filename}'.format(
                        user_id=instance.owner.id,
                        album_id=instance.album.id,
                        filename=filename)
    

class Image(models.Model):
    img = models.ImageField(upload_to=_path_to_file, max_length=257,
                            width_field='width', height_field='height')

    width = models.PositiveSmallIntegerField(default=650)
    height = models.PositiveSmallIntegerField(default=750)

    title = models.TextField(blank=True, default='')
    description = models.TextField(blank=True, default='')
    time_created = models.DateTimeField(auto_now_add=True)
    time_updated = models.DateTimeField(auto_now=True)

    album = models.ForeignKey('albums.Album', null=True, related_name='images')

    owner = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='images')

    users_like = models.ManyToManyField(settings.AUTH_USER_MODEL, related_name='liked_images')

    def __str__(self):
        return self.title
