from django.forms.models import ModelForm, inlineformset_factory
from django.contrib.auth.models import User

from gallery.models.gniuser import GNIUser


class UserProfileForm(ModelForm):

    class Meta:
        model = User
        fields = ('first_name', 'last_name', 'email')


class GNIUserProfileForm(ModelForm):
    
    class Meta:
        model = GNIUser
        fields = ('avatar', 'twitter')
