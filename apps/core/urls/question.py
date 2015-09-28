from django.conf.urls import url
from apps.question import views
from ..views.question import CoreQuestionCreateView


urlpatterns = [

    url(r'^create/$', CoreQuestionCreateView.as_view(), name='create'),
    url(r'^save/$', views.SaveQuestionView.as_view(), name='save'),
    url(r'^edit/(?P<question_id>[0-9]+)$', views.EditQuestionView.as_view(), name='edit'),
    url(r'^update/$', views.UpdateQuestionView.as_view(), name='update'),
    url(r'^show/(?P<question_id>[0-9]+)$', views.ShowQuestionView.as_view(), name='show'),
    url(r'^comment_reply/$', views.CommentReplayView.as_view(), name='comment_reply'),
    url(r'^update_reply/$', views.UpdateReplyView.as_view(), name='update_reply'),


]