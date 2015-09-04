from django.conf.urls import url
from ..views.article import CoreArticleEditView
from apps.article import urls


# To edit or create
_article_edit_view = CoreArticleEditView.as_view()

urlpatterns = [
    url(r'^article/create', urls.article_edit_view, name='create'),
    url(r'^article/edit/(?P<article_id>\d+)$', _article_edit_view, name='edit'),
    url(r'^article/(?P<article_slug>[a-z0-9]+(?:-[a-z0-9]+)*)/(?P<article_id>\d+)$', _article_edit_view, name='view'),
]