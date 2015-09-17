from django.http import Http404
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.views.generic import View
from apps.question.models import Question
from service.forms import CreateQuestionForm, EditQuestionForm, \
    CommentReplyForm, EditAnswerForm
from apps.question.service import business
from django.contrib import messages
from django.utils.translation import ugettext as _
from django.core.urlresolvers import reverse


class CreateQuestionView(View):
    @method_decorator(login_required)
    def get(self, request):
        return render(request, 'question/create.html')

    @method_decorator(login_required)
    def post(self, request):
        form = CreateQuestionForm(request.user, request.POST)
        if not form.process():
            messages.add_message(request, messages.WARNING, _("Question not created!"))
        else:
            messages.add_message(request, messages.SUCCESS, _("Question created successfully!"))
            return redirect(reverse('question:show', args=(form.instance.id,)))

        return render(request, 'question/create.html', {'form': form})


class ListQuestionsView(View):
    def get(self, request):
        questions = Question.objects.all()
        return render(request, 'question/list.html', {'questions': questions})


class SaveQuestionView(View):
    @method_decorator(login_required)
    def post(self, request):
        form = CreateQuestionForm(request.user, request.POST)
        if not form.process():
            messages.add_message(request, messages.WARNING, _("Question not created!"))
        else:
            messages.add_message(request, messages.SUCCESS, _("Question created successfully!"))
            return redirect(reverse('question:show', args=(form.instance.id,)))

        return render(request, 'question/create.html', {'form': form})


class EditQuestionView(View):
    @method_decorator(login_required)
    def get(self, request, question_id):
        question = business.get_question(question_id)
        if question:
            form = EditQuestionForm(instance=question)
            context = {'form': form, 'question': question}
            return render(request, 'question/edit.html', context)
        else:
            messages.add_message(request, messages.WARNING, _("Question is not exists!"))

            return redirect(reverse('question:show', args=question.id))


class UpdateQuestionView(View):
    @method_decorator(login_required)
    def post(self, request):
        question = business.get_question(request.POST['question_id'])
        if question:
            form = EditQuestionForm(data=request.POST, instance=question)
            form.set_author(request.user)
            if form.process():
                messages.add_message(
                    request,
                    messages.SUCCESS,
                    _("Question updated successfully!")
                )

            return render(request, 'question/edit.html', {
                'form': form,
                'question': question
            })
        else:
            messages.add_message(
                request,
                messages.WARNING,
                _("Question is not exists!")
            )

            return redirect(
                reverse('question:show', args=(request.POST["question_id"],))
            )


class ShowQuestionView(View):
    def get(self, request, question_id):
        question = business.get_question(question_id)
        if not question:
            raise Http404(_("Question is not exists!"))

        return render(request, 'question/question-show.html', {'question': question})


class CommentReplayView(View):
    @method_decorator(login_required)
    def post(self, request):
        form = CommentReplyForm(request.POST, request.user)
        if not form.process():
            messages.add_message(request, messages.WARNING, _("Answer not created!"))
            return render(
                request,
                'question/edit_answer.html',
                {
                    'form': form
                }
            )
        else:
            messages.add_message(request, messages.SUCCESS, _("Answer created!"))
            return redirect(
                reverse('question:show', args=(request.POST["question_id"],)))


class UpdateReplyView(View):
    @method_decorator(login_required)
    def post(self, request):
        answer = business.get_answer(request.POST['reply_id'])
        if answer:
            form = EditAnswerForm(instance=answer, data=request.POST)
            form.set_author(request.user)
            if form.process():
                messages.add_message(request, messages.SUCCESS, _("Answer updated successfully!"))
                return redirect(reverse('question:show', args=(form.instance.question.id,)))

            context = {
                'form': form,
                'reply': answer
            }
            return render(request, 'question/edit_answer.html', context)

        else:
            messages.add_message(request, messages.WARNING, _("Answer not exists!"))
            return redirect(
                reverse('question:show', args=(answer.question.id,)))
