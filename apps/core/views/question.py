__author__ = 'phillip'
from apps.question import views
from ..forms.question import CoreQuestionForm

class CoreQuestionCreateView(views.CreateQuestionView):

    form = CoreQuestionForm

