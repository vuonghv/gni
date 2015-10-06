import os
import shutil

from django.views.generic import ListView, DetailView
from django.views.generic.detail import SingleObjectMixin
from django.views.generic.edit import (
        CreateView, DeleteView, UpdateView, FormView, ModelFormMixin
)
from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import login_required
from django.core.urlresolvers import reverse_lazy, reverse
from django.core.exceptions import PermissionDenied
from django.conf import settings
from django.http import HttpResponseRedirect
from django.contrib import messages
from django.shortcuts import get_object_or_404

from albums.models import Album
from images.forms import ImageForm
from images.models import Image


class ListAlbum(ListView):
    model = Album
    template_name = 'albums/list.html'
    context_object_name = 'albums'

    def get_queryset(self):
        """
        Retrieve all albums order by time_created
        """
        queryset = self.model.objects.order_by('-time_created')
        return queryset


class DetailAlbum(DetailView):
    model = Album
    context_object_name = 'album'
    template_name = 'albums/detail.html'

    def get_context_data(self, **kwargs):
        # TODO: Need to optimize querying database
        context = super().get_context_data(**kwargs)
        context['images'] = self.object.images.order_by('-time_created')
        return context


class CreateAlbum(CreateView):
    model = Album
    fields = ['title', 'description']
    template_name = 'albums/new.html'

    @method_decorator(login_required)
    def dispatch(self, *args, **kwargs):
        return super().dispatch(*args, **kwargs)

    def get_success_url(self):
        return reverse_lazy('users:home')

    def form_valid(self, form):
        form.instance.owner = self.request.user
        return super().form_valid(form)


class UpdateAlbum(UpdateView):
    model = Album
    fields = ['title', 'description',]
    template_name = 'albums/edit.html'
    context_object_name = 'album'

    @method_decorator(login_required)
    def dispatch(self, *args, **kwargs):
        return super().dispatch(*args, **kwargs)

    def get_success_url(self):
        return reverse_lazy('albums:detail',
                    kwargs={'pk': self.object.pk})

    def form_valid(self, form):
        if form.instance.owner != self.request.user:
            raise PermissionDenied(
                    'You have NO permissions to edit the album.')
        form.instance.thumbnail = None
        return super().form_valid(form)


class DeleteAlbum(DeleteView):
    # TODO: Need to implement this view so that ONLY OWNER of
    # the album can delete it.
    # And, also delete the album folder
    # I wonder If Images database is deleted?
    model = Album
    context_object_name = 'album'
    template_name = 'albums/confirm_delete_form.html'
    success_url = reverse_lazy('albums:index')

    @method_decorator(login_required)
    def dispatch(self, *args, **kwargs):
        return super().dispatch(*args, **kwargs)

    def can_delete(self, request):
        """
        Check if request.user can delete the album
        """
        self.object = self.get_object()
        return self.object.owner == request.user

    def delete(self, request, *args, **kwargs):
        """
        Override the method of baseclass DeletionMixin
        """
        if not self.can_delete(request):
            raise PermissionDenied(
                    'You have NO permissions to delete the album')

        return super().delete(request, *args, **kwargs)


class AddImage(SingleObjectMixin, FormView):
    model = Album
    form_class = ImageForm
    context_object_name = 'album'
    template_name = 'albums/add_image.html'

    @method_decorator(login_required)
    def dispatch(self, request, *args, **kwargs):
        self.object = self.get_object()
        return super().dispatch(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        if self.object.owner != request.user:
            raise PermissionDenied('You cannot add images to this album!')
        return super().post(request, *args, **kwargs)

    def get_success_url(self):
        return reverse_lazy('albums:detail', kwargs={'pk': self.object.pk})

    def form_valid(self, form):
        form.instance.album = self.object
        form.instance.owner = self.request.user
        form.save()
        messages.success(self.request, 'Post image successfully',
                    extra_tags='alert alert-success')
        return super().form_valid(form)


def set_thumbnail(request, pk):
    if request.method == 'POST':
        album = get_object_or_404(Album, pk=pk)
        image = get_object_or_404(Image, pk=request.POST.get('image'))
        album.thumbnail = image
        album.save()
        messages.success(request, 'Update thumbnail successfully.',
                        extra_tags='alert alert-success')
    return HttpResponseRedirect(reverse('albums:detail', kwargs={'pk': pk}))
