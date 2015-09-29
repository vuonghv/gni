import os

from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import (
        UserCreationForm,
        AuthenticationForm,
        UserChangeForm,
)
from django.views.generic import DetailView, ListView
from django.views.generic.detail import SingleObjectMixin
from django.views.generic.edit import CreateView, UpdateView
from django.core.urlresolvers import reverse_lazy, reverse
from django.core.exceptions import PermissionDenied
from django.core import paginator
from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from django.utils.decorators import method_decorator
from django.conf import settings

from gallery.models.gniuser import GNIUser
from gallery.forms.users import UserProfileForm, GNIUserProfileForm


class SignupUser(CreateView):
    model = settings.AUTH_USER_MODEL
    form_class = UserCreationForm
    template_name = 'users/signup.html'

    def get_success_url(self):
        return reverse_lazy('users:signin')

    """
    def form_valid(self, form):
        self.object = form.save()
        guser = GNIUser.objects.create(user=self.object)
        guser.save()

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
    """


def signin(request):
    if request.method == 'POST':
        signin_form = AuthenticationForm(data=request.POST)

        if signin_form.is_valid():
            user = signin_form.get_user()
            login(request, user)
            # TODO: need to change redirect in the future.
            return HttpResponseRedirect(reverse('users:signup'))

    else:
        signin_form = AuthenticationForm()

    return render(request, 'users/signin.html', {'form': signin_form})


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
    form_class = UserProfileForm
    template_name = 'user/update_profile.html'
    context_object_name = 'user_obj'

    @method_decorator(login_required)
    def dispatch(self, *args, **kwargs):
        return super().dispatch(*args, **kwargs)

    def get_success_url(self):
        return reverse_lazy('gallery:detail-user',
                            kwargs={'pk': self.object.pk})

    def get(self, request, *args, **kwargs):
        """
        Handles GET requests and instantiates the fields of forms with
        associated model's data.
        """
        self.object = self.get_object()
        form = self.get_form()
        guser_form = GNIUserProfileForm(instance=self.object.gniuser)
        return self.render_to_response(
                self.get_context_data(form=form, guser_form=guser_form))

    def post(self, request, *args, **kwargs):
        """
        Handles POST requests and update data of forms with the passed
        POST adn FILES variables and the checked for validity.
        """
        self.object = self.get_object()
        form = self.get_form()
        guser_form = GNIUserProfileForm(instance=self.object.gniuser,
                                        data=self.request.POST,
                                        files=self.request.FILES)

        if form.is_valid() and guser_form.is_valid():
            return self.form_valid(form, guser_form)
        else:
            return self.form_invalid(form, guser_form)

    def form_valid(self, form, guser_form):
        """
        If the form is valid, and form.instance is current user,
        save the associated model and re-direct to the success_url.
        """
        if form.instance.pk != self.request.user.pk:
            raise PermissionDenied(
                    'You have no permissions to edit user %s' % form.instance)

        self.object = form.save()
        guser_form.save()
        return HttpResponseRedirect(self.get_success_url())

    def form_invalid(self, form, guser_form):
        """
        If the form is invalid, re-render the context data with the
        data-filled form and errors.
        """
        return self.render_to_response(
                self.get_context_data(form=form, guser_form=guser_form))


class UserListAlbum(SingleObjectMixin, ListView):
    template_name = 'user/list_album.html'
    context_object_name = 'user_obj'
    paginate_by = 9

    def get(self, request, *args, **kwargs):
        self.object = self.get_object(queryset=User.objects.all())
        return super().get(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context[self.context_object_name] = self.object
        return context

    def get_queryset(self):
        return self.object.albums.order_by('-time_updated')


class UserListImage(SingleObjectMixin, ListView):
    template_name = 'user/list_image.html'
    context_object_name = 'user_obj'
    paginate_by = 3

    def get(self, request, *args, **kwargs):
        self.object = self.get_object(queryset=User.objects.all())
        return super().get(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context[self.context_object_name] = self.object
        return context

    def get_queryset(self):
        return self.object.images.order_by('-time_created')
