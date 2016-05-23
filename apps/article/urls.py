from django.conf.urls import url

from . import views

article_edit_view = views.ArticleEditView.as_view()
article_show_view = views.ArticleView.as_view()
article_delete_view = views.ArticleDeleteView.as_view()

urlpatterns = [
    url(r'^article/create', article_edit_view, name='create'),
    url(r'^article/(?P<article_id>\d+)/edit$', article_edit_view, name='edit'),
    url(r'^(?P<year>\d\d\d\d+)/(?P<month>(0[1-9]|[1-2][0-9]|3[0-1]))/(?P<slug>[aA-zZ0-9-_]+).html$', article_show_view, name='view'),
    url(r'^article/(?P<article_id>\d+)/delete$', article_delete_view, name='delete'),
]