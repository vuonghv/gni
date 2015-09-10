from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.contrib.auth.forms import (
        UserCreationForm,
        AuthenticationForm,
        UserChangeForm,
)
from django.views.generic.edit import CreateView, UpdateView
from django.core.urlresolvers import reverse_lazy, reverse
from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from django.utils.decorators import method_decorator


class SignupUser(CreateView):
    model = User
    form_class = UserCreationForm
    template_name = 'user/signup.html'

    def get_success_url(self):
        return reverse_lazy('gallery:index')


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


class UpdateProfileUser(UpdateView):
    model = User
    #form_class = UserChangeForm
    fields = ['first_name', 'last_name', 'email']
    template_name = 'user/update_profile.html'

    @method_decorator(login_required)
    def dispatch(self, *args, **kwargs):
        return super().dispatch(*args, **kwargs)

    def get_success_url(self):
        return reverse_lazy('gallery:index')
