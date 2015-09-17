from django.apps import AppConfig


class GalleryConfig(AppConfig):
    name = 'gallery'
    verbose_name = 'GNI is Not Instagram'

    def ready(self):
        import gallery.signals.images
        import gallery.signals.albums
