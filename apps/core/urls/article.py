from django.conf.urls import url
from django.utils.translation import ugettext_lazy as _
from ..views.article import views, CoreArticleEditView, CoreArticleView, CoreArticleInCommunityView

_article_show_view = views.ArticleView.as_view()
_article_edit_view = CoreArticleEditView.as_view()
_article_delete_view = views.ArticleDeleteView.as_view()
_article_create_in_community = CoreArticleInCommunityView.as_view()

urlpatterns = [
    # Translators: URL de criacao de artigo
    url(_(r'^article/create$'), _article_edit_view, name='create'),
    # Translators: URL de edicao de artigo
    url(_(r'^article/edit/(?P<article_id>\d+)$'), _article_edit_view, name='edit'),
    # Translators: URL de delecao de artigo
    url(_(r'^article/delete/(?P<article_id>\d+)$'), _article_delete_view, name='delete'),
    # Translators: URL de delecao assincrona de artigo
    url(_(r'^article/delete/async/(?P<article_id>\d+)$'), views.ArticleDeleteAjax.as_view(), name='delete-async'),
    # Translators: URL de criacao de artigo
    url(_(r'^article/(?P<article_id>\d+)/(?P<article_slug>[a-z0-9]+(?:-[a-z0-9]+)*)$'), CoreArticleView.as_view(), name='view'),

    # Translators: URL de criacao de artigo em uma comunidade
    url(_(r'^article/create/(?P<community_slug>[a-z0-9]+(?:-[a-z0-9]+)*)$'), _article_create_in_community, name='create-in-category'),
]