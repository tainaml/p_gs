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
    url(r'^comunidade$', views.community, name='comunidade'),
    url(r'^comunidade/membros$', views.community_members, name='comunidade-membros'),
    url(r'^comunidade/about$', views.community_about, name='comunidade-sobre'),
    url(r'^comunidade/videos$', views.community_videos, name='comunidade-videos'),
    url(r'^comunidade/perguntas$', views.community_question, name='comunidade-perguntas'),
    url(r'^notificacoes$', views.notifications, name='notificacao'),
    url(r'^notificacoes/membros$', views.member_notifications, name='notificacao-membros'),
    url(r'^notificacoes/perguntas-e-respostas$', views.questions_and_answers_notifications, name='notificacao-perguntas-e-respostas'),
    url(r'^criar-artigo$', views.write_article, name='criar-artigo'),
    url(r'^criar-pergunta$', views.write_question, name='criar-pergunta'),
    url(r'^post$', views.post, name='post'),
    url(r'^question$', views.question, name='question'),
    url(r'^search$', views.search, name='pesquisa'),
    url(r'^categoria$', views.category, name='categoria'),
]