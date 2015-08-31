from django.conf.urls import include, url
from . import views

urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'^perfil$', views.perfil, name='perfil'),
    url(r'^perfil/feed$', views.feed, name='feed'),
    url(r'^perfil/about$', views.about, name='about'),
    url(r'^perfil/relationship$', views.relationship, name='relationship'),
    url(r'^perfil/communities$', views.communities, name='communities'),
    url(r'^perfil/videos$', views.videos, name='videos'),
]