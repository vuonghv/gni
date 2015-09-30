from django.forms import ModelForm, Textarea

from comments.models import Comment


class CommentImageForm(ModelForm):

    class Meta:
        model = Comment
        fields = ('content',)
        widgets = {
                'content': Textarea(attrs={'cols': 30, 'rows': 3}),
        }
