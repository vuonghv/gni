import os
import shutil
import hashlib

from django.views.generic import ListView, DetailView
from django.views.generic.edit import CreateView, DeleteView, UpdateView
from django.utils import timezone
from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import login_required
from django.core.urlresolvers import reverse_lazy, reverse
from django.core.exceptions import PermissionDenied
from django.core.files import uploadedfile
from django.conf import settings
from django.http import HttpResponseRedirect

from gallery.models.image import Image


class CreateImage(CreateView):
    model = Image
    fields = ['title', 'description', 'img', 'album']
    template_name = 'image/create_image.html'

    @method_decorator(login_required)
    def dispatch(self, *args, **kwargs):
        return super().dispatch(*args, **kwargs)

    def get_success_url(self):
        return reverse_lazy('gallery:detail-album',
                        kwargs={'pk': self.object.album.id})

    def form_valid(self, form):
        form.instance.owner = self.request.user

        name, ext = os.path.splitext(form.instance.img.name)
        sha512 = hashlib.sha512()
        sha512.update(bytes(form.instance.img.name, encoding='utf-8'))
        sha512.update(bytes(str(timezone.now()), encoding='utf-8'))

        filename = sha512.hexdigest()
        form.instance.img.name = filename + ext

        #ploaded_file = self.request.FILES['img']
        #ith open(form.instance.img.path, 'wb+') as disk_file:
        #   for chunk in uploaded_file.chunks():
        #       disk_file.write(chunk)

        self.object = form.save()

        return super().form_valid(form)


class DetailImage(DetailView):
    model = Image
    context_object_name = 'image'
    template_name = 'image/detail_image.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['comments'] = self.object.comments.all()
        context['users_like'] = self.object.users_like.all()
        if self.request.user in context['users_like']:
            context['liked'] = True
        else:
            context['liked'] = False

        return context
