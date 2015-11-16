from django.conf.urls import url
from apps.question import views
from ..views import question as CoreViews
from ..views.question import CoreQuestionCreateView


urlpatterns = [

    url(r'^create/$', CoreViews.CoreQuestionCreateView.as_view(), name='create'),
    url(r'^save/$', CoreViews.CoreSaveQuestionView.as_view(), name='save'),
    url(r'^edit/(?P<question_id>[0-9]+)$', CoreViews.CoreEditQuestionView.as_view(), name='edit'),
    url(r'^update/$', CoreViews.CoreUpdateQuestionView.as_view(), name='update'),
    url(r'^comment_reply/$', views.CommentReplayView.as_view(), name='comment_reply'),
    url(r'^update_reply/$', views.UpdateReplyView.as_view(), name='update_reply'),
    url(r'^load/related/(?P<question_id>[0-9]+)/(?P<content_type>[a-z]+)/$', CoreViews.CoreQuestionRelatedView.as_view(), name='related-questions-async'),

    url(r'^(?P<question_slug>[a-z0-9]+(?:(-|_)[a-z0-9]+)*)/(?P<question_id>[0-9]+)/$', views.ShowQuestionView.as_view(), name='show')

]