__author__ = 'phillip'
from apps.question import views
from ..forms import question as QuestionForms

class CoreQuestionCreateView(views.CreateQuestionView):
    form = QuestionForms.CoreCreateQuestionForm


class CoreSaveQuestionView(views.SaveQuestionView):
    form = QuestionForms.CoreCreateQuestionForm


class CoreEditQuestionView(views.EditQuestionView):
    form = QuestionForms.CoreEditQuestionForm


class CoreUpdateQuestionView(views.UpdateQuestionView):
    form = QuestionForms.CoreEditQuestionForm

