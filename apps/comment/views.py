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

    def get_context(self, request=None, instance=None):
        return {}


class CommentIndexView(CommentBaseView):

    template_path = 'comment/index_teste.html'

    def get(self, request):
        user = User.objects.all()[0]

        context = {'user': user}
        context.update(self.get_context(request))

        return render(request, self.template_path, context)


class CommentSaveView(CommentBaseView):

    template_path = 'comment/create.html'
    comment_template_path = 'comment/comment.html'
    form_comment = CreateCommentForm


    @method_decorator(login_required)
    def post(self, request):

        if 'content_object_id' not in request.POST \
                or 'content_type' not in request.POST:
            raise Http404()

        form = self.form_comment(request.user, request.POST)

        instance = form.process()
        validation = True if instance else False

        context = {}
        response_data = {}
        if validation:
            self.template_path = self.comment_template_path
            context['comment'] = instance

        else:
            response_data['errors'] = form.errors

        context.update(self.get_context(request))

        response_data['validation'] = validation
        response_data['template'] = render(request, self.template_path, context).content

        return JsonResponse(response_data, status=200 if validation else 400)



class CommentUpdateView(CommentBaseView):

    template_path = 'comment/create.html'
    form_comment = EditCommentForm

    @method_decorator(login_required)
    def post(self, request):
        if 'next_url' not in request.POST or 'comment_id' not in request.POST:
            raise Http404()

        comment = Business.retrieve_own_comment(comment_id=request.POST['comment_id'],
                                                user=request.user)
        if not comment:
            raise self.not_found

        form = self.form_comment(request.user, request.POST['comment_id'], request.POST)

        context = {'form': form}
        context.update(self.get_context(request))

        if not form.process():
            return render(request, self.template_path, context)

        return redirect(request.POST['next_url'])


class CommentDeleteView(CommentBaseView):

    @method_decorator(login_required)
    def get(self, request, comment_id):

        comment = Business.retrieve_own_comment(comment_id=comment_id, user=request.user)

        if comment:
            Business.delete_comment(comment)
        else:
            raise self.not_found

        return redirect(reverse('comment:index_teste'))

class CommentListView(CommentBaseView):

    template_path = 'comment/list-comment.html'

    @method_decorator(login_required)
    def get(self, request):

        itens_by_page = 10

        comments = Business.get_comments_by_content_type_and_id(
                request.GET['content_type'],
                request.GET['content_id'],
                itens_by_page,
                request.GET['page']
        )


        return render(request, self.template_path, {'comments': comments})

class CommentAnswerView(CommentListView):

    template_path = 'comment/list-answer.html'

class AnswerSaveView(CommentSaveView):
    template_path = 'comment/create.html'
    comment_template_path = 'comment/comment-child.html'