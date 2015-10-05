from django.conf.urls import url

from . import views


urlpatterns = [
        url(r'^$', views.ListAlbum.as_view(), name='index'),
        url(r'^new/$', views.CreateAlbum.as_view(), name='new'),
        url(r'^(?P<pk>[0-9]+)/$', views.DetailAlbum.as_view(), name='detail'),
        url(r'^(?P<pk>[0-9]+)/edit/$', views.UpdateAlbum.as_view(), name='edit'),
        url(r'^(?P<pk>[0-9]+)/delete/$', views.DeleteAlbum.as_view(), name='delete'),
        url(r'^(?P<pk>[0-9]+)/add/$', views.AddImage.as_view(), name='add'),
]
