# -*- coding: utf-8 -*-
import copy

from django.contrib.auth.decorators import login_required
from django.core.urlresolvers import reverse
from django.http import Http404, JsonResponse, HttpResponse
from django.shortcuts import render, redirect
from django.utils.decorators import method_decorator
from django.utils.translation import ugettext as _
from django.views.generic import View

from .service.forms import CreateCommentForm, EditCommentForm, ListCommentForm
from .service import business as comment_business

class CommentListBaseView(View):

    xhr = False
    itens_by_page = 10
    context = {}
    response_data = {}
    form = ListCommentForm

    @property
    def template_list_path(self):
        raise NotImplementedError("you must specify the template_list_path property")

    def do_process(self, request=None):


        self.response_data['template'] = render(request,
                                           self.template_list_path,
                                           self.context).content


        return render(request, self.template_list_path, self.context)


class CommentList(CommentListBaseView):
    xhr = True
    template_list_path = 'comment/list-comment.html'

    def get(self, request=None):

        form = self.form(self.itens_by_page, request.GET)
        instance_list = form.process()


        if not form.is_valid():
            print form.errors
            raise Http404()

        self.context.update({
            'comments': instance_list,
            'form': form,
            'page': form.cleaned_data['page'] + 1}
        )



        return super(CommentList, self).do_process(request)


class CommentAnswerList(CommentList):
    xhr = True
    template_list_path = 'comment/list-answer.html'


class CommentFormBaseView(View):
    not_found = Http404(_('Comment not Found.'))
    instance = None
    context = {}
    xhr = False
    form = None

    @property
    def success_template_path(self):
        raise NotImplementedError("you must specify the success_template_path")

    @property
    def fail_validation_template_path(self):
        raise NotImplementedError(
            "you must specify the fail_validation_template_path")

    def do_process(self, request=None, *args, **kwargs):

        if self.form:
            self.instance = self.form.process()
            self.context.update({'instance': self.instance, 'form': self.form})
            is_valid = not not self.instance

            if self.xhr:
                response_data = {}
                if is_valid:
                    response_data['is_valid'] = is_valid
                    response_data['template'] = render(request,
                                                       self.success_template_path,
                                                       self.context).content
                else:
                    response_data['errors'] = self.form.errors
                    print response_data['errors']

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


class CommentSaveView(CommentFormBaseView):
    fail_validation_template_path = 'comment/create.html'
    success_template_path = 'comment/comment.html'
    form_comment = CreateCommentForm
    xhr = True

    @method_decorator(login_required)
    def post(self, request=None):
        if 'content_object_id' not in request.POST \
                or 'content_type' not in request.POST:
            raise Http404()


        self.form = self.form_comment(request.user, request.POST)

        return super(CommentSaveView, self).do_process(request)

class CommentSaveAnswer(CommentFormBaseView):
    fail_validation_template_path = 'comment/create-answer.html'
    success_template_path = 'comment/comment-child.html'
    form_comment = CreateCommentForm
    xhr = True

    @method_decorator(login_required)
    def post(self, request=None):
        if 'content_object_id' not in request.POST:
            raise Http404()

        self.form = self.form_comment(request.user, request.POST)

        return super(CommentSaveAnswer, self).do_process(request)

class CommentUpdateView(CommentFormBaseView):
    fail_validation_template_path = 'comment/edit-comment.html'
    success_template_path = 'comment/comment-segment.html'

    form_comment = EditCommentForm
    xhr = True

    @method_decorator(login_required)
    def post(self, request=None):
        comment = comment_business.retrieve_own_comment(
            comment_id=request.POST['comment_id'],
            user=request.user)

        if not comment:
            raise Http404()

        self.form = self.form_comment(request.user, request.POST['comment_id'],
                                      request.POST)

        return super(CommentUpdateView, self).do_process(request)


class CommentUpdateAnswerView(CommentFormBaseView):
    fail_validation_template_path = 'comment/edit-answer.html'
    success_template_path = 'comment/comment-child-segment.html'

    form_comment = EditCommentForm
    xhr = True

    @method_decorator(login_required)
    def post(self, request=None):
        comment = comment_business.retrieve_own_comment(
            comment_id=request.POST['comment_id'],
            user=request.user)

        if not comment:
            raise Http404()

        self.form = self.form_comment(request.user, request.POST['comment_id'],
                                      request.POST)

        return super(CommentUpdateAnswerView, self).do_process(request)


class CommentDeleteView(CommentFormBaseView):
    @method_decorator(login_required)
    def get(self, request=None, comment_id=None, *args, **kwargs):

        comment = comment_business.retrieve_own_comment(comment_id=comment_id,
                                                        user=request.user)

        if comment:
            comment_business.delete_comment(comment)
        else:
            raise self.not_found

        return redirect(reverse('comment:index_teste'))

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

