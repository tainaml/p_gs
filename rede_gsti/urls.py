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

url_statics = static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
url_media = static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

urlpatterns = [
    url(r'^admin/', include(admin.site.urls)),
    url(r'^account/', include('apps.account.urls', namespace='account')),
    url(r'^comment/', include('apps.comment.urls', namespace='comment')),
    url(r'^profile/', include('apps.userprofile.urls', namespace='profile')),
    url(r'^socialaccount/', include('apps.socialaccount.urls', namespace='socialaccount')),
    url(r'^socialactions/', include('apps.socialactions.urls', namespace='socialactions')),
    url('', include('social.apps.django_app.urls', namespace='social')),
    url(r'^articles/', include('apps.article.urls', namespace='article')),
    url(r'^ninico/', include('apps.ninico.urls', namespace='ninico')),
    url(r'^question/', include('apps.question.urls', namespace='question')),
] + url_statics + url_media
