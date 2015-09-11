from django.views.generic.base import TemplateView

from .albums import Album


class GalleryIndex(TemplateView):
    template_name = 'gallery/index.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        
        user = self.request.user
        if user.is_authenticated():
            context['album_list'] = user.albums.order_by('-time_created')
        else:
            context['album_list'] = Album.objects.order_by('-time_created')

        # TODO: Get timeline photo

        return context
