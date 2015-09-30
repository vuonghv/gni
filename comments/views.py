from django.views.generic import ListView, DetailView, View
from django.views.generic.detail import SingleObjectMixin
from django.views.generic.edit import (
        CreateView, DeleteView, UpdateView, DeletionMixin
)
from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import login_required
from django.core.urlresolvers import reverse_lazy, reverse
from django.core.exceptions import PermissionDenied
from django.http import HttpResponseRedirect

from comments.models import Comment
from comments.forms import CommentImageForm


class LikeComment(SingleObjectMixin, View):
    """
    Record the current user's liking a comment.
    """
    model = Comment

    @method_decorator(login_required)
    def dispatch(self, request, *args, **kwargs):
        super().dispatch(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        self.object = self.get_object()
        self.object.users_like.add(request.user)
        return HttpResponseRedirect(reverse('images:detail',
                                    kwargs={'pk': self.object.image.pk}))

    def put(self, request, *args, **kwargs):
        return self.post(request, *args, **kwargs)


class UnlikeComment(SingleObjectMixin, View):
    """
    Remove the current user's unliking a comment.
    """
    model = Comment

    @method_decorator(login_required)
    def dispatch(self, request, *args, **kwargs):
        super().dispatch(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        self.object = self.get_object()
        self.object.users_like.remove(request.user)
        return HttpResponseRedirect(reverse('images:detail',
                                    kwargs={'pk': self.object.image.pk}))

    def put(self, request, *args, **kwargs):
        return self.post(request, *args, **kwargs)


class DeleteComment(SingleObjectMixin, DeletionMixin, View):
    model = Comment
    
    def get_success_url(self):
        return reverse_lazy('images:detail',
                            kwargs={'pk': self.object.image.pk})

    def delete(self, request, *args, **kwargs):
        self.object = self.get_object()
        if self.object.owner != request.user:
            raise PermissionDenied('You can not delete the comment!') 
        return super().delete(request, *args, **kwargs)


class UpdateComment(UpdateView):
    model = Comment
    fields = ['content',]
    template_name = 'comments/edit.html'

    @method_decorator(login_required)
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)

    def get_success_url(self):
        return reverse_lazy('images:detail',
                            kwargs={'pk': self.object.image.pk})

    def form_valid(self, form):
        if form.instance.owner.pk != self.request.user.pk:
            raise PermissionDenied(
                    'You have no permissions to edit this comment!')
        return super().form_valid(form)
