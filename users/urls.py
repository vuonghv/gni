from django.conf.urls import url

from . import views


urlpatterns = [
        url(r'^home/$', views.HomePage.as_view(), name='home'),
        url(r'^signup/$', views.SignupUser.as_view(), name='signup'),
        url(r'^login/$', views.signin, name='signin'),
        url(r'^logout/$', views.signout, name='signout'),
        url(r'^(?P<pk>[0-9]+)/$', views.DetailUser.as_view(), name='detail'),
        url(r'^(?P<pk>[0-9]+)/edit/$', views.UpdateProfileUser.as_view(), name='edit'),
        url(r'^(?P<pk>[0-9]+)/albums/$', views.UserListAlbum.as_view(), name='albums'),
        url(r'^(?P<pk>[0-9]+)/images/$', views.UserListImage.as_view(), name='images'),
]
