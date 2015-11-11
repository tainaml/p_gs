from django.conf.urls import url
from django.views.decorators.cache import cache_page
from ..views.article import views, CoreArticleEditView
from apps.article import urls

_article_show_view = views.ArticleView.as_view()
_article_edit_view = CoreArticleEditView.as_view()
_article_delete_view = views.ArticleDeleteView.as_view()

urlpatterns = [
    url(r'^article/create$', urls.article_edit_view, name='create'),
    url(r'^article/edit/(?P<article_id>\d+)$', _article_edit_view, name='edit'),
    url(r'^article/delete/(?P<article_id>\d+)$', _article_delete_view, name='delete'),
    url(r'^article/delete/async/(?P<article_id>\d+)$', views.ArticleDeleteAjax.as_view(), name='delete-async'),
    url(r'^article/(?P<article_slug>[a-z0-9]+(?:-[a-z0-9]+)*)/(?P<article_id>\d+)$',cache_page(604800)(_article_show_view), name='view'),
]