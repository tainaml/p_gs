from django.core.exceptions import PermissionDenied
from django.http import Http404, JsonResponse, HttpResponseForbidden
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.views.generic import View
from django.contrib import messages
from django.utils.translation import ugettext as _
from django.core.urlresolvers import reverse

from apps.question.models import Question, Answer
from service.forms import CreateQuestionForm, EditQuestionForm, \
    CommentReplyForm, EditAnswerForm, ListAnswerForm, RemoveAnswerForm
from apps.question.service import business
from .service.business import get_question


class FormBaseView(View):
    not_found = Http404(_('Question not Found.'))
    instance = None
    context = {}

    form = None

    @property
    def success_template_path(self):
        raise NotImplementedError("you must specify the success_template_path")

    def do_process(self, request=None, *args, **kwargs):

        if self.form:
            self.instance = self.form.process()
            self.context.update({'instance': self.instance, 'form': self.form})
            is_valid = not not self.instance

            if request.is_ajax():
                response_data = {}
                if is_valid:
                    response_data['is_valid'] = is_valid
                    response_data['template'] = render(request,
                                                       self.success_template_path,
                                                       self.context).content
                else:
                    response_data['errors'] = self.form.errors

                return JsonResponse(response_data,
                                    status=200 if is_valid else 400, *args,
                                    **kwargs)
            else:

                return render(request,
                              self.success_template_path if is_valid else
                              self.fail_validation_template_path,
                              self.context,
                              *args,
                              **kwargs)

        return render(request,
                      self.success_template_path,
                      self.context,
                      *args,
                      **kwargs)


class ListBaseView(View):

    itens_by_page = 10
    context = {}
    response_data = {}
    form = ListAnswerForm

    @property
    def template_list_path(self):
        raise NotImplementedError("you must specify the template_list_path property")

    def do_process(self, request=None):
        self.response_data['template'] = render(request,
                                                self.template_list_path,
                                                self.context).content

        return render(request, self.template_list_path, self.context)


class AnswerList(ListBaseView):
    template_list_path = 'comment/list-comment.html'

    def get(self, request=None):

        if 'question_id' in request.GET:
            question = get_question(request.GET['question_id'])
        else:
            raise Http404()

        form = self.form(question, self.itens_by_page, request.GET)
        instance_list = form.process()

        if not form.is_valid():
            raise Http404()

        self.context.update({
            'answers': instance_list,
            'form': form,
            'page': form.cleaned_data['page'] + 1}
        )

        return super(AnswerList, self).do_process(request)


class CreateQuestionView(View):
    form = CreateQuestionForm

    def prepare_context(self, request, context):
        return context

    def prepare_initial_data(self, initial):
        return initial

    @method_decorator(login_required)
    def get(self, request):

        initial_data = self.prepare_initial_data({})

        form = self.form(user=request.user, initial=initial_data)

        _context = {
            'form': form,
        }

        return render(request, 'question/create.html', self.prepare_context(request, _context))

    @method_decorator(login_required)
    def post(self, request):
        form = self.form(data=request.POST, user=request.user)

        _context = {
            'form': form,
        }

        if not form.process():
            messages.add_message(request, messages.WARNING, _("Question not created!"), 'question')
        else:
            messages.add_message(request, messages.SUCCESS, _("Question created successfully!"), 'question')
            return redirect(reverse('question:edit', args=[form.instance.id]))

        return render(request, 'question/create.html', self.prepare_context(request, _context))


class ListQuestionsView(View):
    def get(self, request):
        questions = Question.objects.all()
        return render(request, 'question/list.html', {'questions': questions})


class SaveQuestionView(View):

    form = CreateQuestionForm

    @method_decorator(login_required)
    def post(self, request):
        form = self.form(request.POST, user=request.user)
        if not form.process():
            messages.add_message(request, messages.WARNING, _("Question not created!"), 'question')
        else:
            messages.add_message(request, messages.SUCCESS, _("Question created successfully!"), 'question')

            return redirect(reverse('question:edit', args=[form.instance.id]))

        return render(request, 'question/create.html', {'form': form})


class EditQuestionView(View):

    form = EditQuestionForm

    def prepare_context(self, request, context):
        return context

    @method_decorator(login_required)
    def get(self, request, question_id):
        question = business.get_question(question_id)

        if not question:
            raise Http404(_("Question is not exists!"))

        if not (question.author_id == request.user.id) and not request.user.has_perm('question.change_other_questions'):
            return HttpResponseForbidden()

        form = self.form(user=request.user, instance=question)
        context = {'form': form, 'question': question}
        return render(request, 'question/edit_question.html', self.prepare_context(request, context))


class UpdateQuestionView(View):

    form = EditQuestionForm

    @method_decorator(login_required)
    def post(self, request):

        question_id = request.POST.get('question_id', None)
        question = business.get_question(question_id)

        if not question:
            raise Http404(_("Question is not exists!"))

        if not (question.author_id == request.user.id) and not request.user.has_perm('question.change_other_questions'):
            return HttpResponseForbidden()

        form = self.form(data=request.POST, instance=question, user=request.user)
        if form.process():
            messages.add_message(request, messages.SUCCESS,
                                 _("Question updated successfully!"), 'question-edit')
            return redirect(reverse('question:edit', args=[question.id]))
        else:
            messages.add_message(request, messages.ERROR, 'Erro ao carregar question', 'question-edit')

        return render(request, 'question/edit_question.html', {
            'form': form,
            'question': question
        })


class ShowQuestionView(View):

    template_name = 'question/question-show.html'

    def get_context(self, request, question_instance=None):
        return {}

    def get(self, request, question_slug, question_id):

        prefetch = (
            'author', 'author__profile',
            'author__profile__occupation',
        )

        related = (
            'author'
        )

        question = business.get_question(question_id, prefetch=prefetch, related=related)

        if not question or (question and question.slug != question_slug):
            raise Http404(_("Question is not exists!"))

        answers = business.get_all_answers_by_question(question, prefetch=prefetch, related=related)

        form_answer = EditAnswerForm()

        context = {'question': question, 'answers': answers, 'form_answer': form_answer}
        context.update(self.get_context(request, question))
        return render(request, self.template_name, context)


class CommentReplayView(FormBaseView):

    success_template_path = 'question/partials/answer-show.html'

    @method_decorator(login_required)
    def post(self, request):
        question = business.get_question(request.POST["question_id"])
        if not question:
            raise Http404(_("Question not found"))

        self.form = CommentReplyForm(request.POST, request.user)

        return super(CommentReplayView, self).do_process(request)


class UpdateReplyView(FormBaseView):

    success_template_path = 'question/partials/answer-show.html'

    @method_decorator(login_required)
    def post(self, request):
        answer = business.get_answer(request.POST['reply_id'])

        if answer:
            self.form = EditAnswerForm(instance=answer, user=request.user, data=request.POST)
            return super(UpdateReplyView, self).do_process(request)

        else:
            raise Http404()


class CorrectAnswer(View):

    def get(self, request, answer_id):

        try:
            question = business.set_correct_answer(answer_id)
        except Question.DoesNotExist:
            raise Http404(_("Question is not exists!"))
        except Answer.DoesNotExist:
            raise Http404(_("Answer is not exists!"))

        return redirect(reverse('question:show', args=[question.slug, question.id]))


class RemoveAnswer(View):

    @method_decorator(login_required)
    def post(self, request):

        answer = business.get_answer(request.POST["item-id"])
        if not answer:
            if request.is_ajax():
                return JsonResponse({
                    'errors': _("Answer not found!")
                }, status=400)
            raise Http404(_("Answer not found"))

        form = RemoveAnswerForm({
            'answer': answer.id
        })

        if form.process():
            response_data = {'status': 'ok'}
            return JsonResponse(response_data, status=200)

        response_data = {'errors': form.errors}
        return JsonResponse(response_data, status=400)
