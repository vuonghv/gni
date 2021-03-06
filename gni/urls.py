"""gni URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.8/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Add an import:  from blog import urls as blog_urls
    2. Add a URL to urlpatterns:  url(r'^blog/', include(blog_urls))
"""
from django.conf.urls import include, url
from django.contrib import admin
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    url(r'^users/', include('users.urls', namespace='users')),
    url(r'^albums/', include('albums.urls', namespace='albums')),
    url(r'^images/', include('images.urls', namespace='images')),
    url(r'^comments/', include('comments.urls', namespace='comments')),
    url(r'^admin/', include(admin.site.urls)),

] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
