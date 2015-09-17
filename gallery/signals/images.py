from django.db.models.signals import post_delete
from django.dispatch import receiver

from gallery.models import Image


@receiver(post_delete, sender=Image)
def delete_image_callback(sender, instance, using, **kwargs):
    """
    The function delete image file associated with an image object
    """
    if instance.img:
        instance.img.delete(save=False)
