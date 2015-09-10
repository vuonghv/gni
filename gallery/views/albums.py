from django.views.generic import ListView, DetailView
from django.views.generic.edit import CreateView, DeleteView

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
    pass


class CreateAlbum(CreateView):
    pass


class DeleteView(DeleteView):
    pass
