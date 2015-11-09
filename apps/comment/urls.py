from django.conf.urls import url
from . import views

urlpatterns = [

    url(r'^save/$', views.CommentSaveView.as_view(), name='save'),
    url(r'^answer-save/$', views.CommentSaveAnswer.as_view(), name='answer-save'),
    url(r'^edit/$', views.CommentUpdateView.as_view(), name='edit'),
    url(r'^edit-answer/$', views.CommentUpdateAnswerView.as_view(), name='edit-answer'),
    url(r'^list/$', views.CommentList.as_view(), name='list'),
    url(r'^list-answer/$', views.CommentAnswerList.as_view(), name='list-answer'),
    url(r'^update/$', views.CommentUpdateView.as_view(), name='update'),
    url(r'^list/$', views.CommentList.as_view(), name='list'),
    url(r'^delete/(\d+)/$', views.CommentDeleteView.as_view(), name='delete'),

    url(r'^count/(?P<object_to_link>\d+)/(?P<content_type>[a-z]+)$', views.CommentCountView.as_view(), name='count')
]