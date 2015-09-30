import os
import shutil

from django.dispatch import receiver
from django.db.models.signals import post_save, post_delete
from django.conf import settings

from users.models import UserProfile


@receiver(post_save, sender=settings.AUTH_USER_MODEL)
def create_user_profile(sender, instance, created, raw, using, update_fields, **kwargs):
    """
    Creat a Profile for User when a newly user is created,
    and create avatar and timeline folders.
    """
    if not created:
        return

    profile = UserProfile.objects.create(user=instance)
    profile.save()

    avatar_dir = os.path.join(settings.MEDIA_ROOT,
                          str(instance.pk),
                          settings.AVATAR_DIR_NAME)
    
    timeline_dir = os.path.join(settings.MEDIA_ROOT,
                            str(instance.pk),
                            settings.TIMELINE_DIR_NAME)
    try:
        os.makedirs(avatar_dir, mode=0o700)
        os.makedirs(timeline_dir, mode=0o700)
    except OSError as err:
        print('Created user\'s directory error: {}'.format(err.strerror))


@receiver(post_delete, sender=settings.AUTH_USER_MODEL)
def delete_user_profile(sender, instance, using, **kwargs):
    user_folder = os.path.join(settings.MEDIA_ROOT, str(instance.pk))
    try:
        shutil.rmtree(user_folder)
    except (OSError, Exception) as err:
        print('Delete user\'s directory error: {}'.format(err.strerror))