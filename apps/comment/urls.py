from django.conf.urls import url
from . import views

urlpatterns = [

    url(r'^save/$', views.CommentSaveView.as_view(), name='save'),
    url(r'^update/$', views.CommentUpdateView.as_view(), name='update'),
    url(r'^list/$', views.CommentList.as_view(), name='list'),
    url(r'^delete/(\d+)/$', views.CommentDeleteView.as_view(), name='delete'),

    url(r'^count/(?P<object_to_link>\d+)/(?P<content_type>[a-z]+)$', views.CommentCountView.as_view(), name='count')
]