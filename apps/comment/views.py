# -*- coding: utf-8 -*-

from django.contrib.auth.decorators import login_required
from django.core.urlresolvers import reverse
from django.http import Http404, JsonResponse, HttpResponse
from django.shortcuts import render, redirect
from django.utils.decorators import method_decorator
from django.utils.translation import ugettext as _
from django.views.generic import View
from apps.custom_base.views import FormBaseView, InstanceSaveFormBaseView, InstanceUpdateFormBaseView, FormBaseListView

from .service.forms import CreateCommentForm, EditCommentForm, ListCommentForm
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

        # self.response_data['template'] = render(request,
        #                                    self.template_list_path,
        #                                    self.context).content

        return render(request, self.template_list_path, self.context)


class CommentList(FormBaseListView):
    success_template_path = 'comment/list-comment.html'
    fail_template_path = 'comment/list-comment.html'
    form = ListCommentForm
    itens_by_page = 4

    # @Override
    def fill_form_kwargs(self, request=None, *args, **kwargs):
        return {'data': request.GET, 'itens_by_page': self.itens_by_page}

   # @Override
    def after_process(self, request=None, *args, **kwargs):
        self.context.update({'comments': self.process_return})


class CommentAnswerList(CommentList):
    xhr = True
    template_list_path = 'comment/list-answer.html'

class CommentSaveView(InstanceSaveFormBaseView):
    fail_validation_template_path = 'comment/create.html'
    success_template_path = 'comment/comment.html'
    form = CreateCommentForm


class CommentSaveAnswer(InstanceSaveFormBaseView):
    fail_validation_template_path = 'comment/create-answer.html'
    success_template_path = 'comment/comment-child.html'
    form = CreateCommentForm

class CommentUpdateView(InstanceUpdateFormBaseView):

    fail_validation_template_path = 'comment/edit-comment.html'
    success_template_path = 'comment/comment-segment.html'
    form = EditCommentForm

    def instance_to_update(self, request, *args, **kwargs):
        return comment_business.retrieve_own_comment(
            comment_id=request.POST['comment_id'],
            user=request.user)


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

