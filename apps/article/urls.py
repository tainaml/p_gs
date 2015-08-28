from django.conf.urls import url
from . import views


urlpatterns = [
    url(r'^article/new', views.article_edit, name='create'),
    url(r'^article/edit/(?P<article_slug>[a-z0-9]+(?:-[a-z0-9]+)*)/(?P<article_id>\d+)$', views.article_edit, name='edit'),
    url(r'^article/save$', views.article_save, name='save'),
]