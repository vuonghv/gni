from django.conf.urls import url

from .views import albums, users, gallery, images, comments


urlpatterns = [
    url(r'^$', gallery.GalleryIndex.as_view(), name='index'),

    url(r'^signup/$', users.SignupUser.as_view(), name='signup'),
    url(r'^signin/$', users.signin, name='signin'),
    url(r'^signout/$', users.signout, name='signout'),
    url(r'^users/(?P<pk>[0-9]+)/$', users.DetailUser.as_view(), name='detail-user'),
    url(r'^users/(?P<pk>[0-9]+)/edit$', users.UpdateProfileUser.as_view(), name='profile'),
    url(r'^users/(?P<pk>[0-9]+)/albums/$', users.UserListAlbum.as_view(), name='user-list-albums'),

    url(r'^albums/$', albums.ListAlbum.as_view(), name='list-albums'),
    url(r'^albums/new/$', albums.CreateAlbum.as_view(), name='create-album'),
    url(r'^albums/(?P<pk>[0-9]+)/$', albums.DetailAlbum.as_view(), name='detail-album'),
    url(r'^albums/(?P<pk>[0-9]+)/edit/$', albums.UpdateAlbum.as_view(), name='update-album'),
    url(r'^albums/(?P<pk>[0-9]+)/delete/$', albums.DeleteAlbum.as_view(), name='delete-album'),

    url(r'^images/new/$', images.CreateImage.as_view(), name='create-image'),
    url(r'^images/(?P<pk>[0-9]+)/$', images.DetailImage.as_view(), name='detail-image'),
    url(r'^images/(?P<pk>[0-9]+)/like/$', images.LikeImage.as_view(), name='like-image'),
    url(r'^images/(?P<pk>[0-9]+)/unlike/$', images.UnlikeImage.as_view(), name='unlike-image'),

    url(r'^comments/image/$', comments.CreateComment.as_view(), name='create-comment'),
    url(r'^comments/(?P<pk>[0-9]+)/like/$', comments.LikeComment.as_view(), name='like-comment'),
    url(r'^comments/(?P<pk>[0-9]+)/unlike/$', comments.UnlikeComment.as_view(), name='unlike-comment'),

]
