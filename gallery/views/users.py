import os

from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.contrib.auth.forms import (
        UserCreationForm,
        AuthenticationForm,
        UserChangeForm,
)
from django.views.generic import DetailView
from django.views.generic.edit import CreateView, UpdateView
from django.core.urlresolvers import reverse_lazy, reverse
from django.core.exceptions import PermissionDenied
from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from django.utils.decorators import method_decorator
from django.conf import settings


class SignupUser(CreateView):
    model = User
    form_class = UserCreationForm
    template_name = 'user/signup.html'

    def get_success_url(self):
        return reverse_lazy('gallery:index')

    def form_valid(self, form):
        self.object = form.save()
        avatar_dir = os.path.join(settings.MEDIA_ROOT,
                              str(self.object.id),
                              settings.AVATAR_DIR_NAME)
        
        timeline_dir = os.path.join(settings.MEDIA_ROOT,
                                str(self.object.id),
                                settings.TIMELINE_DIR_NAME)
        try:
            os.makedirs(avatar_dir, mode=0o700)
            os.makedirs(timeline_dir, mode=0o700)
        except OSError as e:
            print('OSError: %s' % e.strerror)

        return super().form_valid(form)


def signin(request):
    if request.method == 'POST':
        signin_form = AuthenticationForm(data=request.POST)

        if signin_form.is_valid():
            user = authenticate(username=signin_form.cleaned_data['username'],
                                password=signin_form.cleaned_data['password'])

            if user is not None:
                if user.is_active:
                    login(request, user)
                    return HttpResponseRedirect(reverse('gallery:index'))
                else:
                    return HttpResponse('Your account [%s] is disable!' %
                                        user.username)
            else:
                return HttpResponse('Invalid username or password!')

        else:
            HttpResponse(signin_form.errors)

    else:
        signin_form = AuthenticationForm()

    return render(request, 'user/signin.html', {'form': signin_form})


@login_required
def signout(request):
    logout(request)
    return HttpResponseRedirect(reverse('gallery:index'))


class DetailUser(DetailView):
    model = User
    context_object_name = 'user_obj'
    template_name = 'user/detail_user.html'


class UpdateProfileUser(UpdateView):
    model = User
    fields = ['first_name', 'last_name', 'email']
    template_name = 'user/update_profile.html'
    context_object_name = 'user_obj'

    @method_decorator(login_required)
    def dispatch(self, *args, **kwargs):
        return super().dispatch(*args, **kwargs)

    def get_success_url(self):
        return reverse_lazy('gallery:detail-user',
                            kwargs={'pk': self.object.pk})

    def form_valid(self, form):
        if form.instance.pk != self.request.user.pk:
            raise PermissionDenied(
                    'You have no permissions to edit user %s' % form.instance)
        return super().form_valid(form)


class UserListAlbum(DetailView):
    model = User
    template_name = 'user/list_album.html'

    # Need to set context_object_name to avoid conficting 'user' object
    # in 'gallery/base_generic.html'.
    context_object_name = 'user_obj'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['user_albums'] = self.object.albums.all()
        return context
