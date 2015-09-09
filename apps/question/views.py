from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from apps.question.models import Question
from service.forms import CreateQuestionForm, EditQuestionForm, \
    CommentReplyForm
from apps.question.service import business as Business
from django.contrib import messages
from django.utils.translation import ugettext as _
from django.core.urlresolvers import reverse


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
    form = CreateQuestionForm(request.POST, request.user)
    if not form.process():
        return render(request, '../../question/create.html', {'form': form})

    return redirect('../../question/create.html')


@login_required
def edit_question(request, question_id):
    question = Business.get_question(question_id)
    if question:
        form = EditQuestionForm(request.POST)
        return render(request, 'question/edit.html',
        {
            'form': form,
            'question_id': question.id,
            'title': question.title,
            'description': question.description
        })
    else:
        messages.add_message(request, messages.WARNING, _("Question is not exists!"))
        return redirect(reverse('question:edit', args=question.id))

@login_required
def update_question(request):
    question = Business.get_question(request.POST['question_id'])
    if question:
        form = EditQuestionForm(question, request.POST)
        if form.process():
            messages.add_message(request, messages.SUCCESS, _("Question updated successfully!"))
            return redirect(reverse('question:edit'))
        return render(request, 'question/edit.html', {'form': form})
    else:
        messages.add_message(request, messages.WARNING, _("Question is not exists!"))
        return redirect(reverse('question:edit', args=request.POST["question_id"]))


def show_question(request, question_id):
    question = Business.get_question(question_id)
    if question:
        return render(request, 'question/show.html', {'question': question})
    else:
        messages.add_message(request, messages.WARNING, _("Question is not exists!"))
        return redirect(reverse('question:show', args=request.POST["question_id"]))


@login_required
def comment_reply(request):
    form = CommentReplyForm(request.POST, request.user)
    if not form.process():
        return render(request, '../../question/show.html', {'form': form})

    return redirect(reverse('question:show', args=request.POST["question_id"]))



@login_required
def update_reply(request):
    pass