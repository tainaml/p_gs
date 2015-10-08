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
from apps.comment import views as CommentView


url_statics = static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
url_media = static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

urlpatterns = [

    url(r'^admin/', include(admin.site.urls)),
    url(r'^account/', include('apps.account.urls', namespace='account')),

    url(r'^comment/', include('apps.comment.urls', namespace='comment')),

    url(r'^comment/comment-list/', CommentView.CommentListView.as_view(), name='comment-list'),
    url(r'^comment/answer-list/', CommentView.CommentAnswerView.as_view(), name='answer-list'),
    url(r'^comment/answer-save/', CommentView.AnswerSaveView.as_view(), name='answer-save'),


    url(r'^profile/', include('apps.userprofile.urls', namespace='profile')),
    url(r'^socialaccount/', include('apps.socialaccount.urls', namespace='socialaccount')),
    url(r'^socialactions/', include('apps.socialactions.urls', namespace='socialactions')),
    url('', include('social.apps.django_app.urls', namespace='social')),
    url(r'^community/', include('apps.core.urls.community', namespace='community')),
    url(r'^notifications/', include('apps.core.urls.notifications', namespace='notifications')),
    url(r'^', include('apps.core.urls.article', namespace='article')),
    url(r'^ninico/', include('apps.ninico.urls', namespace='ninico')),
    url(r'^question/', include('apps.core.urls.question', namespace='question')),
    url(r'^contact/', include('apps.contact.urls', namespace='contact')),
    url('^mailmanager/', include('apps.mailmanager.urls', namespace='mailmanager')),
    url('^complaint/', include('apps.complaint.urls', namespace='complaint')),

] + url_statics + url_media
