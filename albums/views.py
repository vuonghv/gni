import os
import shutil

from django.views.generic import ListView, DetailView
from django.views.generic.edit import CreateView, DeleteView, UpdateView
from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import login_required
from django.core.urlresolvers import reverse_lazy, reverse
from django.core.exceptions import PermissionDenied
from django.conf import settings
from django.http import HttpResponseRedirect

from albums.models import Album


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
