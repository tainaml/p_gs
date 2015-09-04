from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from apps.question.models import Question


def list_questions(request):
    questions = Question.objects.all()
    return render(request, 'question/list.html', {'questions': questions})


#TODO 'see how filter model'
def list_question(request):
    question = Question.objects.
    return render(request, 'question/index_teste.html', {'question': question})

@login_required
def create_question(request):


@login_required
def save_question(request):


@login_required
def edit_question(request):


@login_required
def update_question(request):


def show_reply(request):


@login_required
def create_reply(request):


@login_required
def save_reply(request):


@login_required
def edit_reply(request):


@login_required
def update_reply(request):