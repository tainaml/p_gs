# -*- coding: utf-8 -*-

from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.core.urlresolvers import reverse
from django.http import Http404, JsonResponse
from django.shortcuts import render, redirect
from django.utils.decorators import method_decorator
from django.utils.translation import ugettext as _
from django.views.generic import View

from .service.forms import CreateCommentForm, EditCommentForm
from .service import business as Business


class CommentBaseView(View):
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
        raise NotImplementedError("you must specify the fail_validation_template_path")

    @property
    def instance_label(self):
        raise NotImplementedError("you must specify the instance_label")

    def __do_process__(self, request=None, *args, **kwargs):

        if self.form:
            self.instance = self.form.process()
            self.context[self.instance_label] = self.instance
            self.context['form'] = self.form
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
                    response_data['template'] = render(request,
                                                       self.fail_validation_template_path,
                                                       self.context).content

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

    def get(self, request=None, *args, **kwargs):
        return self.__do_process__(request, *args, **kwargs)

    def post(self, request=None, *args, **kwargs):
        return self.__do_process__(request, *args, **kwargs)


class CommentIndexView(CommentBaseView):
    template_path = 'comment/index_teste.html'

    def get(self, request=None, *args, **kwargs):
        user = User.objects.all()[0]

        context = {'user': user}

        return render(request, self.template_path, context)


class CommentSaveView(CommentBaseView):
    fail_validation_template_path = 'comment/create.html'

    success_template_path = 'comment/comment.html'
    form_comment = CreateCommentForm
    instance_label = 'comment'
    xhr = True

    @method_decorator(login_required)
    def post(self, request=None, *args, **kwargs):

        if 'content_object_id' not in request.POST \
                or 'content_type' not in request.POST:
            raise Http404()

        self.form = self.form_comment(request.user, request.POST)

        return super(CommentSaveView, self).post(request, *args, **kwargs)


class CommentUpdateView(CommentBaseView):
    template_path = 'comment/create.html'
    form_comment = EditCommentForm

    @method_decorator(login_required)
    def post(self, request):
        if 'next_url' not in request.POST or 'comment_id' not in request.POST:
            raise Http404()

        comment = Business.retrieve_own_comment(
            comment_id=request.POST['comment_id'],
            user=request.user)
        if not comment:
            raise self.not_found

        form = self.form_comment(request.user, request.POST['comment_id'],
                                 request.POST)

        context = {'form': form}

        if not form.process():
            return render(request, self.template_path, context)

        return redirect(request.POST['next_url'])


class CommentDeleteView(CommentBaseView):
    @method_decorator(login_required)
    def get(self, request=None, comment_id=None, *args, **kwargs):

        comment = Business.retrieve_own_comment(comment_id=comment_id,
                                                user=request.user)

        if comment:
            Business.delete_comment(comment)
        else:
            raise self.not_found

        return redirect(reverse('comment:index_teste'))


class CommentListView(CommentBaseView):
    template_path = 'comment/list-comment.html'

    @method_decorator(login_required)
    def get(self, request=None, *args, **kwargs):
        itens_by_page = 10

        comments = Business.get_comments_by_content_type_and_id(
            request.GET['content_type'],
            request.GET['content_id'],
            itens_by_page,
            request.GET['page']
        )

        self.context['comments'] = comments

        return super(CommentListView, self).get(request)


class CommentAnswerView(CommentListView):
    template_path = 'comment/list-answer.html'


class AnswerSaveView(CommentSaveView):
    template_path = 'comment/create.html'
    comment_template_path = 'comment/comment-child.html'

