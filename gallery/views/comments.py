from django.views.generic import ListView, DetailView, View
from django.views.generic.detail import SingleObjectMixin
from django.views.generic.edit import (
        CreateView, DeleteView, UpdateView, DeletionMixin
)
from django.views.decorators.http import require_http_methods
from django.utils import timezone
from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import login_required
from django.core.urlresolvers import reverse_lazy, reverse
from django.core.exceptions import PermissionDenied
from django.core.files import uploadedfile
from django.conf import settings
from django.http import HttpResponseRedirect, HttpResponseForbidden
from django.shortcuts import get_object_or_404

from gallery.models.comment import Comment
from gallery.forms.comments import CommentImageForm


class LikeComment(SingleObjectMixin, View):
    """
    Record the current user's liking a comment.
    """
    model = Comment

    def post(self, request, *args, **kwargs):
        if not request.user.is_authenticated():
            return HttpResponseForbidden(
                    content=b'You have to sign in to like the comment.')

        self.object = self.get_object()
        self.object.users_like.add(request.user)

        return HttpResponseRedirect(reverse('gallery:detail-image',
                                    kwargs={'pk': self.object.image.pk}))

    def put(self, request, *args, **kwargs):
        return self.post(request, *args, **kwargs)


class UnlikeComment(SingleObjectMixin, View):
    """
    Remove the current user's unliking a comment.
    """
    model = Comment

    def post(self, request, *args, **kwargs):
        if not request.user.is_authenticated():
            return HttpResponseForbidden(
                    content=b'You have to sign in to unlike the comment.')

        self.object = self.get_object()
        self.object.users_like.remove(request.user)

        return HttpResponseRedirect(reverse('gallery:detail-image',
                                    kwargs={'pk': self.object.image.pk}))

    def put(self, request, *args, **kwargs):
        return self.post(request, *args, **kwargs)


class DeleteComment(SingleObjectMixin, DeletionMixin, View):
    model = Comment
    
    def get_success_url(self):
        return reverse_lazy('gallery:detail-image',
                            kwargs={'pk': self.object.image.pk})

    def delete(self, request, *args, **kwargs):
        self.object = self.get_object()
        if self.object.owner != request.user:
            return HttpResponseForbidden(
                    content=b'You can not delete the comment.')

        return super().delete(request, *args, **kwargs)


class UpdateComment(UpdateView):
    model = Comment
    fields = ['content',]
    template_name = 'comment/edit_comment.html'

    @method_decorator(login_required)
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)

    def get_success_url(self):
        return reverse_lazy('gallery:detail-image',
                            kwargs={'pk': self.object.image.pk})

    def form_valid(self, form):
        if form.instance.owner.pk != self.request.user.pk:
            return HttpResponseForbidden(
                    content=b'You have no permissions to edit this comment.')

        return super().form_valid(form)
