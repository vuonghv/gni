import os
import shutil

from django.db.models.signals import post_delete
from django.dispatch import receiver
from django.conf import settings

from gallery.models import Album


@receiver(post_delete, sender=Album)
def delete_album_callback(sender, instance, using, **kwargs):
    """
    The function deletes the directory associated with an album object.
    """
    if not isinstance(instance, sender):
        return

    album_path = os.path.join(settings.MEDIA_ROOT,
                            str(instance.owner.id),
                            str(instance.id))
    try:
        shutil.rmtree(album_path)
    except (OSError, Exception) as err:
        print("Exception in delete_album_callback: %s" % err.strerror)
