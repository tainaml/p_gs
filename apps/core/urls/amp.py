from apps.core.views.amp import AmpCoreArticleView, AmpCoreQuestionView
from django.conf.urls import url
from django.utils.translation import ugettext_lazy as _


urlpatterns = [

    # Translators: URL de criacao de artigo
    url(
        _(r'^(?P<year>\d\d\d\d+)/(?P<month>0[1-9]|1[0-2])/(?P<slug>[aA-zZ0-9-_]+).amp$'),
        view=AmpCoreArticleView.as_view(),
        name='article-single',
    ),

    # Translators: URL visualizacao de pergunta
    url(
        _(r'^(?P<question_slug>[a-z0-9]+(?:(-|_)[a-z0-9]+)*)/(?P<question_id>[0-9]+).amp$'),
        view=AmpCoreQuestionView.as_view(),
        name='question-single'
    ),

]