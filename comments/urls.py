from django.conf.urls import url

from . import views


urlpatterns = [
        url(r'^(?P<pk>[0-9]+)/edit/$', views.UpdateComment.as_view(), name='edit'),
        url(r'^(?P<pk>[0-9]+)/delete/$', views.DeleteComment.as_view(), name='delete'),
        url(r'^(?P<pk>[0-9]+)/like/$', views.LikeComment.as_view(), name='like'),
        url(r'^(?P<pk>[0-9]+)/unlike/$', views.UnlikeComment.as_view(), name='unlike'),

]
