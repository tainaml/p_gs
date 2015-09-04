from django.http import Http404
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from apps.question.models import Question
from service.forms import CreateQuestionForm


def list_questions(request):
    questions = Question.objects.all()
    return render(request, 'question/list.html', {'questions': questions})


#TODO 'see how filter model'
def list_question(request):
    #question = Question.objects.
    #return render(request, 'question/index_teste.html', {'question': question})
    pass


@login_required
def create_question(request):
    return render(request, 'question/create.html')


@login_required
def save_question(request):
    form = CreateQuestionForm(request.question, request.POST)
    if not form.process():
        return render(request, 'question/create.html', {'form': form})

    return redirect(request.POST['next_url'])


@login_required
def edit_question(request):
    pass

@login_required
def update_question(request):
    pass


def show_reply(request):
    pass


@login_required
def create_reply(request):
    pass


@login_required
def save_reply(request):
    pass


@login_required
def edit_reply(request):
    pass


@login_required
def update_reply(request):
    pass