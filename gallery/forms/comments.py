from django.forms import ModelForm, Textarea, TextInput, FileInput

from gallery.models import Comment


class CommentImageForm(ModelForm):

    class Meta:
        model = Comment
        fields = ('content', 'image',)
        widgets = {
                'content': Textarea(attrs={'cols': 40, 'rows': 4}),
                'image': TextInput(attrs={'type': 'hidden'}),
        }
