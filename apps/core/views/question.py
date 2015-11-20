from django.http import JsonResponse
from django.shortcuts import render
from apps.question import views
from ..forms import question as QuestionForms
from ..business import question as BusinessQuestion

class CoreQuestionCreateView(views.CreateQuestionView):
    form = QuestionForms.CoreCreateQuestionForm
    pass


class CoreSaveQuestionView(views.SaveQuestionView):
    form = QuestionForms.CoreCreateQuestionForm


class CoreEditQuestionView(views.EditQuestionView):
    form = QuestionForms.CoreEditQuestionForm


class CoreUpdateQuestionView(views.UpdateQuestionView):
    form = QuestionForms.CoreEditQuestionForm


class CoreQuestionRelatedView(views.View):

    template_path = "question/partials/question-related-questions-list.html"

    def return_success(self, request, context=None):

        if request.is_ajax():

            return JsonResponse({
                'template': render(request, self.template_path, context).content
            }, status=200)


    def get(self, request, question_id, content_type):

        related_list = BusinessQuestion.get_related(question_id, content_type, 4, 1)

        context = {'questions': related_list}

        return self.return_success(request, context)