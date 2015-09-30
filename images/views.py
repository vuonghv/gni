import os
import hashlib

from django.views.generic import ListView, DetailView, View
from django.views.generic.detail import SingleObjectMixin
from django.views.generic.edit import CreateView, FormView, DeleteView, UpdateView
from django.utils import timezone
from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import login_required
from django.core.urlresolvers import reverse_lazy, reverse
from django.core.exceptions import PermissionDenied
from django.conf import settings
from django.http import HttpResponseRedirect, HttpResponseForbidden
from django.shortcuts import get_object_or_404

from images.models import Image
from comments.forms import CommentImageForm


class CreateImage(CreateView):
    model = Image
    fields = ['title', 'description', 'img', 'album']
    template_name = 'images/new.html'

    @method_decorator(login_required)
    def dispatch(self, *args, **kwargs):
        return super().dispatch(*args, **kwargs)

    def get_success_url(self):
        return reverse_lazy('albums:detail',
                        kwargs={'pk': self.object.album.pk})

    def form_valid(self, form):
        # Should I put following checking step in another method?
        if form.instance.album not in self.request.user.albums.all():
            raise PermissionDenied

        form.instance.owner = self.request.user

        name, ext = os.path.splitext(form.instance.img.name)
        sha512 = hashlib.sha512()
        sha512.update(bytes(form.instance.img.name, encoding='utf-8'))
        sha512.update(bytes(str(timezone.now()), encoding='utf-8'))

        filename = sha512.hexdigest()
        form.instance.img.name = filename + ext

        return super().form_valid(form)


class DisplayImage(DetailView):
    model = Image
    template_name = 'images/detail.html'
    context_object_name = 'image'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['comments'] = self.object.comments.all()
        context['users_like'] = self.object.users_like.all()

        if self.request.user in context['users_like']:
            context['liked'] = True
            context['number_others_like'] = context['users_like'].count() - 1
        else:
            context['liked'] = False

        context['form'] = CommentImageForm()
        return context


class CommentImage(SingleObjectMixin, FormView):
    model = Image
    template_name = 'images/detail.html'
    form_class = CommentImageForm

    def post(self, request, *args, **kwargs):
        if not request.user.is_authenticated():
            raise PermissionDenied

        self.object = self.get_object()
        return super().post(request, *args, **kwargs)

    def form_valid(self, form):
        form.instance.image = self.object
        form.instance.owner = self.request.user
        form.save()
        return super().form_valid(form)

    def get_success_url(self):
        return reverse_lazy('images:detail',
                            kwargs={'pk': self.object.pk})

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['comments'] = self.object.comments.all()
        context['users_like'] = self.object.users_like.all()

        if self.request.user in context['users_like']:
            context['liked'] = True
            context['number_others_like'] = context['users_like'].count() - 1
        else:
            context['liked'] = False

        return context


class DetailImage(DetailView):

    def get(self, request, *args, **kwargs):
        view = DisplayImage.as_view()
        return view(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        view = CommentImage.as_view()
        return view(request, *args, **kwargs)
    

class DeleteImage(DeleteView):
    model = Image
    template_name = 'images/confirm_delete_form.html'

    @method_decorator(login_required)
    def dispatch(self, *args, **kwargs):
        return super().dispatch(*args, **kwargs)

    def get_success_url(self):
        return reverse_lazy('albums:detail',
                            kwargs={'pk': self.object.album.pk})

    def can_delete(self, request):
        """
        This method checks if request.user can delete the album.
        """
        if not hasattr(self, 'object'):
            self.object = self.get_object()
        return self.object.owner == request.user

    def delete(self, request, *args, **kwargs):
        """
        Override the method of DeletionMixin baseclass
        """
        if not self.can_delete(request):
            raise PermissionDenied

        return super().delete(request, *args, **kwargs)


class LikeImage(SingleObjectMixin, View):
    """
    Record the current user's liking an image.
    """
    model = Image

    @method_decorator(login_required)
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)
    
    def post(self, request, *args, **kwargs):
        self.object = self.get_object()
        self.object.users_like.add(request.user)
        return HttpResponseRedirect(reverse('images:detail',
                                    kwargs={'pk': self.object.pk}))

    def put(self, request, *args, **kwargs):
        return self.post(request, *args, **kwargs)


class UnlikeImage(SingleObjectMixin, View):
    """
    Remove the current user's liking an image.
    """
    model = Image

    @method_decorator(login_required)
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        self.object = self.get_object()
        self.object.users_like.remove(request.user)
        return HttpResponseRedirect(reverse('images:detail',
                                    kwargs={'pk': self.object.pk}))

    def put(self, request, *args, **kwargs):
        return self.post(request, *args, **kwargs)


class UpdateImage(UpdateView):
    model = Image
    fields = ['title', 'description']
    template_name = 'images/edit.html'

    @method_decorator(login_required)
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)

    def get_success_url(self):
        return reverse_lazy('images:detail',
                            kwargs={'pk': self.object.pk})

    def form_valid(self, form):
        if self.object.owner != self.request.user:
            raise PermissionDenied(
                    'You have no permissions to edit this image!')
        return super().form_valid(form)
