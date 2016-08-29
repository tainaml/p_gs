# -*- coding: utf-8 -*-
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.views.generic import View
from django.shortcuts import render
from django.http import Http404, JsonResponse, HttpResponse

from apps.custom_base.views import InstanceSaveFormBaseView, InstanceUpdateFormBaseView, FormBaseListView, \
    InstanceDeleteFormBaseView

from .service.forms import CreateCommentForm, EditCommentForm, ListCommentForm, CommentDeleteForm
from .service import business as comment_business


class CommentListBaseView(View):

    itens_by_page = 10
    context = {}
    response_data = {}
    form = ListCommentForm

    @property
    def template_list_path(self):
        raise NotImplementedError("you must specify the template_list_path property")

    def do_process(self, request=None):

        return render(request, self.template_list_path, self.context)


class CommentList(FormBaseListView):
    success_template_path = 'comment/list-comment.html'
    form = ListCommentForm
    itens_per_page = 10

    # @Override
    def after_process(self, request=None, *args, **kwargs):
        super(CommentList, self).after_process(*args, **kwargs)
        self.context.update({'comments': self.process_return})


class CommentAnswerList(CommentList):
    success_template_path = 'comment/list-answer.html'
    itens_per_page = 10


class CommentSaveView(InstanceSaveFormBaseView):
    fail_validation_template_path = 'comment/create-comment.html'
    success_template_path = 'comment/show-comment.html'
    form = CreateCommentForm


class CommentSaveAnswer(InstanceSaveFormBaseView):
    fail_validation_template_path = 'comment/create-answer.html'
    success_template_path = 'comment/comment-child.html'
    form = CreateCommentForm


class CommentUpdateView(InstanceUpdateFormBaseView):

    fail_validation_template_path = 'comment/edit-comment.html'
    success_template_path = 'comment/show-comment.html'
    form = EditCommentForm

    def instance_to_update(self, request, *args, **kwargs):
        return comment_business.retrieve_own_comment(
            comment_id=request.POST['comment_id'],
            user=request.user)


class CommentDeleteView(View):

    @method_decorator(login_required)
    def post(self, request):

        form = CommentDeleteForm(author=request.user, data={'comment': request.POST.get('item-id')})
        if form.process():
            response_data = {'status': 'ok'}
            return JsonResponse(response_data, status=200)

        response_data = {'errors': form.errors}
        return JsonResponse(response_data, status=400)


class CommentUpdateAnswerView(CommentUpdateView):
    fail_validation_template_path = 'comment/edit-answer.html'
    success_template_path = 'comment/comment-child-segment.html'


class CommentCountView(CommentListBaseView):

    template_path = ""

    def return_success(self, request, context=None):
        if not context:
            context = {}
        if request.is_ajax():
            context.update({
                'template': context.get('count', 0)
            })
            return JsonResponse(context, status=200)

        return HttpResponse(context.get('count', 0), status=200)

    def get(self, request, object_to_link, content_type):
        count = comment_business.count_comments_by_id_and_content_type(object_to_link, content_type)
        context = {'count': count}
        return self.return_success(request, context)
