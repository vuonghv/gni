import os
import shutil

from django.dispatch import receiver
from django.db.models.signals import post_delete, post_save
from django.conf import settings

from albums.models import Album


@receiver(post_save, sender=Album)
def create_album_dir(sender, instance, created, **kwargs):
    """
    Create a new folder when a new album is inserted in database
    """
    if not created:
        return

    album_dir = os.path.join(settings.MEDIA_ROOT,
                        str(instance.owner.pk),
                        str(instance.pk))
    try:
        os.makedirs(album_dir, mode=0o700)
    except OSError as err:
        print('Create album directory error: {}'.format(err.strerror))


@receiver(post_delete, sender=Album)
def delete_album_dir(sender, instance, using, **kwargs):
    album_dir = os.path.join(settings.MEDIA_ROOT,
                        str(instance.owner.pk),
                        str(instance.pk))
    try:
        shutil.rmtree(album_dir)
    except (OSError, Exception) as err:
        print('Delete album directory error: {}'.format(err.strerror))
