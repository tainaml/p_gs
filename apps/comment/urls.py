from django.conf.urls import url
from . import views

urlpatterns = [

    url(r'^save/$', views.CommentSaveView.as_view(), name='save'),
    url(r'^edit/$', views.CommentUpdateView.as_view(), name='edit'),
    url(r'^list/$', views.CommentList.as_view(), name='list'),
    url(r'^list-answer/$', views.CommentAnswerList.as_view(), name='list-answer'),
    url(r'^update/$', views.CommentUpdateView.as_view(), name='update'),
    url(r'^delete/(\d+)/$', views.CommentDeleteView.as_view(), name='delete')
]