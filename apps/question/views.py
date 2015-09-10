from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from apps.question.models import Question
from service.forms import CreateQuestionForm, EditQuestionForm, \
    CommentReplyForm, EditAnswerForm
from apps.question.service import business
from django.contrib import messages
from django.utils.translation import ugettext as _
from django.core.urlresolvers import reverse


def list_questions(request):
    questions = Question.objects.all()
    return render(request, 'question/list.html', {'questions': questions})


# TODO 'see how filter model'
def list_question(request):
    pass


@login_required
def create_question(request):
    return render(request, 'question/create.html')


@login_required
def save_question(request):
    form = CreateQuestionForm(request.POST, request.user)
    if not form.process():
        messages.add_message(request, messages.WARNING,
                                     _("Question not created!"))
        return redirect(reverse('question:create'))

    messages.add_message(request, messages.SUCCESS,
                             _("Question created sucessfully!"))
    return redirect(reverse('question:create'))


@login_required
def edit_question(request, question_id):
    question = business.get_question(question_id)
    if question:
        form = EditQuestionForm(instance=question)
        return render(
            request,
            'question/edit.html',
            {
                'form': form,
                'question': question
            }
        )
    else:
        messages.add_message(
            request,
            messages.WARNING, _("Question is not exists!")
        )

        return redirect(reverse('question:show', args=question.id))


@login_required
def update_question(request):
    question = business.get_question(request.POST['question_id'])
    if question:
        form = EditQuestionForm(data=request.POST, instance=question)
        form.set_author(request.user)
        if form.process():
            messages.add_message(request, messages.SUCCESS,
                                 _("Question updated successfully!"))
        return render(request, 'question/edit.html',
        {
            'form': form,
            'question': question
        })
    else:
        messages.add_message(request, messages.WARNING,
                             _("Question is not exists!"))
        return redirect(
            reverse('question:show', args=(request.POST["question_id"],)))


def show_question(request, question_id):
    question = business.get_question(question_id)
    if question:
        return render(request, 'question/show.html', {'question': question})
    else:
        messages.add_message(request, messages.WARNING,
                             _("Question is not exists!"))
        return redirect(
            reverse('question:show', args=(request.POST["question_id"],)))


@login_required
def comment_reply(request):
    form = CommentReplyForm(request.POST, request.user)
    if not form.process():
        return render(request, '../../question/show.html', {'form': form})

    return redirect(reverse('question:show', args=(request.POST["question_id"],)))


@login_required
def update_reply(request):
    answer = business.get_answer(request.POST['reply_id'])
    if answer:
        form = EditAnswerForm(instance=answer, data=request.POST)
        if form.process():
            messages.add_message(
                request,
                messages.SUCCESS,
                _("Answer updated successfully!")
            )

        return  render(
            request,
            'question/edit_answer.html',
            {
                'form': form,
                'reply': answer
            }
        )

    else:
        messages.add_message(request, messages.WARNING,
                             _("Answer not exists!"))
        return redirect(
            reverse('question:show', args=(reply.question.id,)))