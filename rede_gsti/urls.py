"""rede_gsti URL Configuration

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
from django.conf.urls.static import static
from django.contrib import admin
from django.conf import settings
from apps.ninico.views import index as PROJECT_ROOT

url_statics = static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
url_media = static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

urlpatterns = [
    url(r'^$', PROJECT_ROOT, name='index'),
    url(r'^admin/', include(admin.site.urls)),
    url(r'^account/', include('apps.core.urls.account', namespace='account')),
    url(r'^comment/', include('apps.comment.urls', namespace='comment')),
    url(r'^profile/', include('apps.core.urls.user', namespace='profile')),
    url(r'^socialaccount/', include('apps.socialaccount.urls', namespace='socialaccount')),
    url(r'^socialactions/', include('apps.socialactions.urls', namespace='socialactions')),
    url('', include('social.apps.django_app.urls', namespace='social')),
    url(r'^community/', include('apps.core.urls.community', namespace='community')),
    url(r'^notifications/', include('apps.core.urls.notifications', namespace='notifications')),
    url(r'^', include('apps.core.urls.article', namespace='article')),
    url(r'^', include('apps.core.urls.socialactions', namespace='core_socialactions')),
    url(r'^ninico/?', include('apps.ninico.urls', namespace='ninico')),
    url(r'^question/', include('apps.core.urls.question', namespace='question')),
    url(r'^contact/', include('apps.core.urls.contact', namespace='contact')),
    url(r'^mailmanager/', include('apps.mailmanager.urls', namespace='mailmanager')),
    url(r'^complaint/', include('apps.complaint.urls', namespace='complaint')),
    url(r'^settings/', include('apps.core.urls.configuration', namespace='configuration')),
    url(r'^feed/', include('apps.core.urls.feed', namespace='feed')),
    url(r'^', include('apps.core.urls.search', namespace='search')),
    url(r'^', include('apps.core.urls.core', namespace='core')),

    url(r'^ckeditor/', include('ckeditor_uploader.urls')),


] + url_statics + url_media
