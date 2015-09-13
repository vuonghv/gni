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

from gallery.models.album import Album


class ListAlbum(ListView):
    model = Album
    template_name = 'album/list_album.html'
    context_object_name = 'album_list'

    def get_queryset(self):
        user = self.request.user
        if user.is_authenticated():
            queryset = user.albums.order_by('-time_created')
        else:
            queryset = self.model.objects.order_by('-time_created')

        return queryset


class DetailAlbum(DetailView):
    model = Album
    context_object_name = 'album'
    template_name = 'album/detail_album.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        return context


class CreateAlbum(CreateView):
    model = Album
    fields = ['title', 'description']
    template_name = 'album/create_album.html'

    @method_decorator(login_required)
    def dispatch(self, *args, **kwargs):
        return super().dispatch(*args, **kwargs)

    def get_success_url(self):
        return reverse_lazy('gallery:index')

    def form_valid(self, form):
        form.instance.owner = self.request.user
        self.object = form.save()

        album_dir = os.path.join(settings.MEDIA_ROOT,
                                str(self.request.user.id),
                                str(self.object.id))

        try:
            os.makedirs(album_dir, mode=0o700)
        except OSError as e:
            print('OSError : %s' % e.strerror)
        
        return super().form_valid(form)


class UpdateAlbum(UpdateView):
    model = Album
    fields = ['title', 'description',]
    template_name = 'album/update_album.html'
    context_object_name = 'album'

    @method_decorator(login_required)
    def dispatch(self, *args, **kwargs):
        return super().dispatch(*args, **kwargs)

    def get_success_url(self):
        return reverse_lazy('gallery:detail-album',
                    kwargs={'pk': self.object.id})

    def form_valid(self, form):
        form.instance.thumbnail = ''
        return super().form_valid(form)


class DeleteAlbum(DeleteView):
    # TODO: Need to implement this view so that ONLY OWNER of
    # the album can delete it.
    # And, also delete the album folder
    # I wonder If Images database is deleted?
    model = Album
    context_object_name = 'album'
    template_name = 'album/confirm_delete_album.html'
    success_url = reverse_lazy('gallery:list-albums')

    @method_decorator(login_required)
    def dispatch(self, *args, **kwargs):
        return super().dispatch(*args, **kwargs)

    def can_delete(self, request):
        """
        Check if request.user can delete the album
        """
        self.object = self.get_object()
        return self.object.owner.pk == request.user.pk

    def delete(self, request, *args, **kwargs):
        """
        Override the method of baseclass DeletionMixin
        """
        if not self.can_delete(request):
            raise PermissionDenied(
                    'You do NOT have permissions to delete the album')

        self.object = self.get_object()
        album_dir = os.path.join(settings.MEDIA_ROOT,
                                str(request.user.id),
                                str(self.object.id))
        # TODO: need to delete Images database related with the album
        try:
            shutil.rmtree(album_dir)
        except (Exception, OSError) as err:
            print("Exception: %s" % err.strerror)

        return super().delete(request, *args, **kwargs)
