from django.forms import ModelForm, Textarea

from images.models import Image


class ImageForm(ModelForm):

    class Meta:
        model = Image
        fields = ('title', 'description', 'img')
        widgets = {
                'title': Textarea(attrs={'cols': 30, 'rows': 3}),
                'description': Textarea(attrs={'cols': 30, 'rows': 3}),
        }
