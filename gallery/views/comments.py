import os
import shutil
import hashlib

from django.views.generic import ListView, DetailView
from django.views.generic.edit import CreateView, DeleteView, UpdateView
from django.views.decorators.http import require_http_methods
from django.utils import timezone
from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import login_required
from django.core.urlresolvers import reverse_lazy, reverse
from django.core.exceptions import PermissionDenied
from django.core.files import uploadedfile
from django.conf import settings
from django.http import HttpResponseRedirect
from django.shortcuts import get_object_or_404

from gallery.models.comment import Comment
from gallery.forms.comments import CommentImageForm


class CreateComment(CreateView):
    model = Comment
    form_class = CommentImageForm

    @method_decorator(login_required)
    def dispatch(self, *args, **kwargs):
        return super().dispatch(*args, **kwargs)

    def get_success_url(self):
        return reverse_lazy('gallery:detail-image',
                            kwargs={'pk': self.object.image.id})

    def get_failure_url(self, form):
        return reverse_lazy('gallery:detail-image',
                            kwargs={'pk': form.instance.image.id})

    def form_valid(self, form):
        form.instance.owner = self.request.user
        return super().form_valid(form)

    def form_invalid(self, form):
        return HttpResponseRedirect(self.get_failure_url(form)) 
