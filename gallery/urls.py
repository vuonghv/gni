from django.conf.urls import url

from .views import albums, users


urlpatterns = [
    url(r'^$', albums.ListAlbum.as_view(), name='index'),
    url(r'^signup/$', users.SignupUser.as_view(), name='signup'),
    url(r'^signin/$', users.signin, name='signin'),
    url(r'^signout/$', users.signout, name='signout'),
    url(r'^users/(?P<pk>[0-9]+)/$', users.UpdateProfileUser.as_view(), name='profile'),
]
