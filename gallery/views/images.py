import os
import shutil
import hashlib

from django.views.generic import ListView, DetailView, View
from django.views.generic.detail import SingleObjectMixin
from django.views.generic.edit import CreateView, DeleteView, UpdateView, FormView
from django.views.decorators.http import require_http_methods
from django.utils import timezone
from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import login_required, permission_required
from django.core.urlresolvers import reverse_lazy, reverse
from django.core.exceptions import PermissionDenied
from django.core.files import uploadedfile
from django.conf import settings
from django.http import HttpResponseRedirect, HttpResponseForbidden
from django.shortcuts import get_object_or_404

from gallery.models.image import Image
from gallery.forms.comments import CommentImageForm


class CreateImage(CreateView):
    model = Image
    fields = ['title', 'description', 'img', 'album']
    template_name = 'image/create_image.html'

    #@method_decorator(permission_required('gallery.add_image', raise_exception=True))
    @method_decorator(login_required)
    def dispatch(self, *args, **kwargs):
        return super().dispatch(*args, **kwargs)

    def get_success_url(self):
        return reverse_lazy('gallery:detail-album',
                        kwargs={'pk': self.object.album.id})

    def get_initial(self):
        initial = super().get_initial()
        return initial

    def form_valid(self, form):
        # Should I put following checking step in another method?
        if form.instance.album not in self.request.user.albums.all():
            return HttpResponseForbidden(
                    content=b'You have no permissions to post an image \
                            on album %s' % str(form.instance.album))

        form.instance.owner = self.request.user

        name, ext = os.path.splitext(form.instance.img.name)
        sha512 = hashlib.sha512()
        sha512.update(bytes(form.instance.img.name, encoding='utf-8'))
        sha512.update(bytes(str(timezone.now()), encoding='utf-8'))

        filename = sha512.hexdigest()
        form.instance.img.name = filename + ext

        self.object = form.save()

        return super().form_valid(form)


class DisplayImage(DetailView):
    model = Image
    template_name = 'image/detail_image.html'
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
    template_name = 'image/detail_image.html'
    form_class = CommentImageForm

    def post(self, request, *args, **kwargs):
        if not request.user.is_authenticated():
            return HttpResponseForbidden(
                    content=b'You have to sign in to comment.')

        self.object = self.get_object()
        return super().post(request, *args, **kwargs)

    def form_valid(self, form):
        form.instance.image = self.object
        form.instance.owner = self.request.user
        form.save()
        return super().form_valid(form)

    def get_success_url(self):
        return reverse_lazy('gallery:detail-image',
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


class LikeImage(SingleObjectMixin, View):
    """
    Record the current user's liking an image.
    """
    model = Image
    
    def post(self, request, *args, **kwargs):

        if not request.user.is_authenticated():
            return HttpResponseForbidden(
                    content=b'You have to sign in to like the image')

        self.object = self.get_object()
        self.object.users_like.add(request.user)

        return HttpResponseRedirect(reverse('gallery:detail-image',
                                    kwargs={'pk': self.object.pk}))

    def put(self, request, *args, **kwargs):
        return self.post(request, *args, **kwargs)


class UnlikeImage(SingleObjectMixin, View):
    """
    Remove the current user's liking an image.
    """
    model = Image

    def post(self, request, *args, **kwargs):

        if not request.user.is_authenticated():
            return HttpResponseForbidden(
                    content=b'You have to sign in to unlike the image.')

        self.object = self.get_object()
        self.object.users_like.remove(request.user)

        return HttpResponseRedirect(reverse('gallery:detail-image',
                                    kwargs={'pk': self.object.pk}))

    def put(self, request, *args, **kwargs):
        return self.post(request, *args, **kwargs)
