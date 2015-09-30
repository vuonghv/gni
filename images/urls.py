from django.conf.urls import url

from . import views


urlpatterns = [
        url(r'^new/$', views.CreateImage.as_view(), name='new'),
        url(r'^(?P<pk>[0-9]+)/$', views.DetailImage.as_view(), name='detail'),
        url(r'^(?P<pk>[0-9]+)/edit/$', views.UpdateImage.as_view(), name='edit'),
        url(r'^(?P<pk>[0-9]+)/delete/$', views.DeleteImage.as_view(), name='delete'),
        url(r'^(?P<pk>[0-9]+)/like/$', views.LikeImage.as_view(), name='like'),
        url(r'^(?P<pk>[0-9]+)/unlike/$', views.UnlikeImage.as_view(), name='unlike'),

]
