from django.conf.urls import url
from apps.core.views.question import CoreQuestionCreateView
from apps.question.views import ShowQuestionView

urlpatterns = [
    url(r'^create', CoreQuestionCreateView.as_view(), name='create'),
    url(r'^show/(?P<question_id>[0-9]+)$', ShowQuestionView.as_view(), name='show')

]