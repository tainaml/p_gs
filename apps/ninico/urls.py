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
    url(r'^perfil/sugestoes$', views.suggestions, name='sugestoes'),
    url(r'^perfil/ver-depois$', views.see_after, name='ver-depois'),
    url(r'^perfil/favoritos$', views.favorites, name='favoritos'),
    url(r'^criar-artigo$', views.write_article, name='criar-artigo'),
    url(r'^criar-pergunta$', views.write_question, name='criar-pergunta'),
    url(r'^post$', views.post, name='post'),
    url(r'^question$', views.question, name='question'),
]