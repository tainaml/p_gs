from django.conf.urls import url
from . import views

urlpatterns = [

    url(r'^index_teste/$', views.CommentIndexView.as_view(), name='index_teste'),
    url(r'^save/$', views.CommentSaveView.as_view(), name='save'),
    url(r'^update/$', views.CommentUpdateView.as_view(), name='update'),
    url(r'^delete/(\d+)/$', views.CommentDeleteView.as_view(), name='delete')
]