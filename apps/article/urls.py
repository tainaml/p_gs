from django.conf.urls import url
from . import views


article_edit_view = views.ArticleEditView.as_view()

urlpatterns = [
    url(r'^article/new', article_edit_view, name='create'),
    url(r'^article/edit/(?P<article_slug>[a-z0-9]+(?:-[a-z0-9]+)*)/(?P<article_id>\d+)$', article_edit_view, name='edit'),
    #url(r'^article/save$', views.article_save, name='save'),
]