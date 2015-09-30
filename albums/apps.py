from django.apps import AppConfig


class AlbumsAppConfig(AppConfig):
    name='albums'
    verbose_name = "User's albums"

    def ready(self):
        from . import signals
