from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.core.urlresolvers import reverse
from django.http import Http404, JsonResponse, HttpResponse
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
    form_comment = CreateCommentForm

    @method_decorator(login_required)
    def post(self, request):

        if 'content_object_id' not in request.POST \
                or 'content_type' not in request.POST \
                or 'next_url' not in request.POST:
            raise Http404()

        form = self.form_comment(request.user, request.POST)

        context = {'form': form}
        context.update(self.get_context(request))

        if not form.process():
            return render(request, self.template_path, context)

        return redirect(request.POST['next_url'])


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


class CommentCountView(CommentBaseView):

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
        count = Business.count_comments_by_id_and_content_type(object_to_link, content_type)
        context = {'count': count}
        return self.return_success(request, context)