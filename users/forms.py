from django.forms import models
from django.conf import settings
from django.apps import apps as django_apps

from users.models import UserProfile


class UserForm(models.ModelForm):

    class Meta:
        model = django_apps.get_model(settings.AUTH_USER_MODEL)
        fields = ('first_name', 'last_name', 'email')


class UserProfileForm(models.ModelForm):

    class Meta:
        model = UserProfile
        fields = ('avatar', 'twitter')
