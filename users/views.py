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
from django.apps import apps as django_apps

#from gallery.models.gniuser import GNIUser
from images.models import Image
from users.forms import UserForm, UserProfileForm


class SignupUser(CreateView):
    model = django_apps.get_model(settings.AUTH_USER_MODEL)
    form_class = UserCreationForm
    template_name = 'users/signup.html'

    def get_success_url(self):
        return reverse_lazy('users:signin')


def signin(request):
    if request.method == 'POST':
        signin_form = AuthenticationForm(data=request.POST)

        if signin_form.is_valid():
            user = signin_form.get_user()
            login(request, user)
            # TODO: need to change redirect in the future.
            return HttpResponseRedirect(reverse('users:home'))

    else:
        signin_form = AuthenticationForm()

    return render(request, 'users/signin.html', {'form': signin_form})


@login_required
def signout(request):
    logout(request)
    return HttpResponseRedirect(reverse('users:home'))


class HomePage(ListView):
    model = Image
    context_object_name = 'images'
    template_name = 'homepage.html'
    paginate_by = 5

    def get_queryset(self):
        if self.request.user.is_authenticated():
            #return self.request.user.images.order_by('-time_created')
            return Image.objects.filter(
                            owner=self.request.user).order_by('-time_created')
        return Image.objects.order_by('-time_created')


class DetailUser(DetailView):
    # TODO: Need to optimize for querying database (!!! duplicated !!!)
    model = django_apps.get_model(settings.AUTH_USER_MODEL)
    context_object_name = 'user_obj'
    template_name = 'users/detail.html'


class UpdateProfileUser(UpdateView):
    model = django_apps.get_model(settings.AUTH_USER_MODEL)
    form_class = UserForm
    template_name = 'users/edit.html'
    context_object_name = 'user_obj'

    @method_decorator(login_required)
    def dispatch(self, *args, **kwargs):
        return super().dispatch(*args, **kwargs)

    def get_success_url(self):
        return reverse_lazy('users:detail', kwargs={'pk': self.object.pk})

    def get(self, request, *args, **kwargs):
        """
        Handles GET requests and instantiates the fields of forms with
        associated model's data.
        """
        self.object = self.get_object()
        user_form = self.get_form()
        profile_form = UserProfileForm(instance=self.object.profile)
        return self.render_to_response(self.get_context_data(
                            form=user_form, profile_form=profile_form))

    def post(self, request, *args, **kwargs):
        """
        Handles POST requests and update data of forms with the passed
        POST adn FILES variables and the checked for validity.
        """
        self.object = self.get_object()
        user_form = self.get_form()
        profile_form = UserProfileForm(instance=self.object.profile,
                                        data=self.request.POST,
                                        files=self.request.FILES)

        if user_form.is_valid() and profile_form.is_valid():
            return self.form_valid(user_form, profile_form)
        else:
            return self.form_invalid(user_form, profile_form)

    def form_valid(self, user_form, profile_form):
        """
        If the form is valid, and form.instance is current user,
        save the associated model and re-direct to the success_url.
        """
        if user_form.instance != self.request.user:
            raise PermissionDenied

        self.object = user_form.save()
        profile_form.save()
        return HttpResponseRedirect(self.get_success_url())

    def form_invalid(self, user_form, profile_form):
        """
        If the form is invalid, re-render the context data with the
        data-filled form and errors.
        """
        return self.render_to_response(self.get_context_data(
                            form=user_form, profile_form=profile_form))


class UserListAlbum(SingleObjectMixin, ListView):
    template_name = 'users/albums.html'
    context_object_name = 'user_obj'
    paginate_by = 9

    def get(self, request, *args, **kwargs):
        user_model = django_apps.get_model(settings.AUTH_USER_MODEL)
        self.object = self.get_object(queryset=user_model.objects.all())
        return super().get(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context[self.context_object_name] = self.object
        return context

    def get_queryset(self):
        return self.object.albums.order_by('-time_updated')


class UserListImage(SingleObjectMixin, ListView):
    template_name = 'users/images.html'
    context_object_name = 'user_obj'
    paginate_by = 3

    def get(self, request, *args, **kwargs):
        user_model = django_apps.get_model(settings.AUTH_USER_MODEL)
        self.object = self.get_object(queryset=user_model.objects.all())
        return super().get(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context[self.context_object_name] = self.object
        return context

    def get_queryset(self):
        return self.object.images.order_by('-time_created')
