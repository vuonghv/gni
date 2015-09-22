from django.views.generic import ListView

from gallery.models.image import Image


class GalleryIndex(ListView):
    model = Image
    template_name = 'gallery/index.html'
    paginate_by = 5

    def get_queryset(self):
        if self.request.user.is_authenticated():
            return self.request.user.images.order_by('-time_created')

        return Image.objects.order_by('-time_created')
