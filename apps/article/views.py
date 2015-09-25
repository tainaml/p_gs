from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.core.urlresolvers import reverse
from django.forms import model_to_dict
from django.http import Http404, HttpResponseForbidden, HttpResponse
from django.core.exceptions import PermissionDenied
from django.shortcuts import render, redirect
from django.utils.decorators import method_decorator
from django.utils.translation import gettext as _
from django.views.generic import View
from .service import business as Business
from .service.forms import ArticleForm


class ArticleBaseView(View):

    article_not_found = Http404(_('Article not Found.'))

    def filter_article(self, request, article_id=None):
        article = Business.get_article(article_id)

        if not article:
            '''
            Only works when article exists
            '''
            raise self.article_not_found

        return article

    def check_is_owner(self, request, article):
        if article.id and not article.author.id == request.user.id :
            '''
            Only the article author has permission to edit article
            '''
            raise PermissionDenied(_('Operation not permitted'))


class ArticleView(ArticleBaseView):

    template_name = 'article/single.html'

    def get(self, request, article_slug, article_id):
        article = self.filter_article(request, article_id)
        if not str(article.slug) == str(article_slug):
            raise self.article_not_found

        return render(request, self.template_name, {'article': article})


class ArticleDeleteView(ArticleBaseView):

    template_name = ''

    def return_error(self, request):
        return HttpResponse(status=401)

    def return_success(self, request):
        return HttpResponse(status=200)

    @method_decorator(login_required)
    def get(self, request, article_id):
        article = self.filter_article(request, article_id)

        # Fail if is not owner
        self.check_is_owner(request, article)

        if not article.id:
            raise self.article_not_found

        if article.status == article.STATUS_TRASH:
            raise self.article_not_found

        if Business.delete_article(article):
            return self.return_error(request)

        return self.return_success(request)


class ArticleEditView(ArticleBaseView):

    template_name = 'article/article-edit.html'
    form_article = ArticleForm

    def prepare_context(self, request, context):
        if not context or not isinstance(context, dict):
            context = {}

        return context

    @method_decorator(login_required)
    def get(self, request, article_id=None, *args, **kwargs):

        article = self.filter_article(request, article_id)

        # Fail if is not owner
        self.check_is_owner(request, article)

        if not article_id:
            article = Business.create_temp_article(request.user)
            return redirect(reverse('article:edit', args=(article.id,)))

        form_article = self.form_article(instance=article)
        _context = {'form_article': form_article, 'article': article}
        return render(request, self.template_name, self.prepare_context(request, _context))

    @method_decorator(login_required)
    def post(self, request, article_id=None, *args, **kwargs):

        article = self.filter_article(request, article_id)
        # Fail if is not owner
        self.check_is_owner(request, article)

        form_article = self.form_article(request.POST, request.FILES, instance=article)
        form_article.set_author(request.user)

        article_saved = form_article.process()

        if article_saved is not False:
            messages.add_message(request, messages.SUCCESS, _('Success'))
            article_id = form_article.instance.id
            return redirect(reverse('article:edit', args=(article_id,)))
        else:
            messages.add_message(request, messages.ERROR, _('Generic Error'))

        _context = {'form_article': form_article, 'article': article}
        return render(request, self.template_name, self.prepare_context(request, _context))