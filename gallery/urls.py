from django.conf.urls import url

from .views import albums, users, gallery, images


urlpatterns = [
    url(r'^$', gallery.GalleryIndex.as_view(), name='index'),

    url(r'^signup/$', users.SignupUser.as_view(), name='signup'),
    url(r'^signin/$', users.signin, name='signin'),
    url(r'^signout/$', users.signout, name='signout'),
    url(r'^users/(?P<pk>[0-9]+)/$', users.UpdateProfileUser.as_view(), name='profile'),

    url(r'^albums/$', albums.ListAlbum.as_view(), name='list-albums'),
    url(r'^albums/new/$', albums.CreateAlbum.as_view(), name='create-album'),
    url(r'^albums/(?P<pk>[0-9]+)/$', albums.DetailAlbum.as_view(), name='detail-album'),
    url(r'^albums/(?P<pk>[0-9]+)/edit/$', albums.UpdateAlbum.as_view(), name='update-album'),
    url(r'^albums/(?P<pk>[0-9]+)/delete/$', albums.DeleteAlbum.as_view(), name='delete-album'),

    url(r'^images/new/$', images.CreateImage.as_view(), name='create-image'),

]
