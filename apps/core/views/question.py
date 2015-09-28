from django.shortcuts import render
from apps.core.forms.question import CoreCreateQuestionForm
from apps.question import views


class CoreQuestionCreateView(views.CreateQuestionView):

    form_question = CoreCreateQuestionForm