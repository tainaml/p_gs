from apps.core.views.article import CoreArticleView
from apps.core.views.question import CoreQuestionView


class AmpCoreArticleView(CoreArticleView):
    template_name = 'core/amp/pages/article.html'


class AmpCoreQuestionView(CoreQuestionView):
    template_name = 'core/amp/pages/question.html'