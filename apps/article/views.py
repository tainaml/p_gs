# coding=utf-8
import copy

from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.core.urlresolvers import reverse
from django.http import Http404, HttpResponse, JsonResponse
from django.core.exceptions import PermissionDenied
from django.shortcuts import render, redirect
from django.utils.decorators import method_decorator
from django.utils.translation import gettext as _
from django.views.generic import View

from apps.article.service.business import get_article
from .service import business as Business
from .service.forms import ArticleForm


class ArticleBaseView(View):

    msg_article_not_found = _('Article not Found.')
    article_not_found = Http404(_('Article not Found.'))

    def filter_article(self, request=None, year=None, month=None, slug=None):
        article = Business.get_article()

        if not article:
            '''
            Only works when article exists
            '''
            raise self.article_not_found

        return article

    def check_is_owner(self, request, article):

        can_edit_others = request.user.has_perm('article.change_other_articles')
        is_author = (article.author_id == request.user.id) if article.id and article.author else False
        is_new_article = article.id is None
        if not is_author and not can_edit_others and not is_new_article:

            '''
            Only the article author has permission to edit article
            '''
            raise PermissionDenied(_('Operation not permitted'))


class ArticleView(ArticleBaseView):

    template_name = 'article/single.html'

    # def dispatch(self, request, *args, **kwargs):
    #     return super(ArticleView, self).dispatch(*args, **kwargs)



    def get_context(self, request, article_instance=None):
        return {}

    def get(self, request, year, month, slug):
        article = self.filter_article(request, slug)

        context = {'article': article}
        context.update(self.get_context(request, article))

        return render(request, self.template_name, context)


class ArticleDeleteView(ArticleBaseView):

    template_name = ''

    def return_error(self, request, context=None):
        return HttpResponse(status=401)

    def return_success(self, request, context=None):
        return HttpResponse(status=200)

    def get_context(self, request, article_instance=None):
        return {}

    @method_decorator(login_required)
    def get(self, request, article_id):
        # article = self.filter_article(request=request, article_id=article_id)
        article = Business.get_article(article_id)

        # Fail if is not owner
        self.check_is_owner(request, article)

        if not article.id:
            raise self.article_not_found

        if article.status == article.STATUS_TRASH:
            raise self.article_not_found

        if Business.delete_article(article):
            return self.return_error(request)

        context = {'article': article}
        context.update(self.get_context(request, article))

        return self.return_success(request, context)


class ArticleDeleteAjax(ArticleDeleteView):

    def return_error(self, request, context=None):
        response_context = context
        return JsonResponse(response_context, status=401)

    def return_success(self, request, context=None):

        response_context = {'status': 200}

        if hasattr(context, 'article'):
            article = context.get('article')
            response_context.update({
                'item_id': article.id,
                'deleted': True if article.status == 2 else False
            })

        return JsonResponse(response_context, status=200)

    @method_decorator(login_required)
    def post(self, request, article_id):

        if article_id != request.POST.get('item-id'):
            context = {
                'status': 401,
                'errors': {
                    '__all__': [self.msg_article_not_found]
                }
            }
            return self.return_error(request, context)

        # article = self.filter_article(request=request, article_id=article_id)
        article = Business.get_article(article_id)

        # Fail if is not owner
        self.check_is_owner(request, article)

        if not article.id:
            context = {
                'status': 401,
                'errors': {
                    '__all__': [self.msg_article_not_found]
                }
            }
            return self.return_error(request, context)

        if article.status == article.STATUS_TRASH:
            context = {
                'status': 400,
                'errors': {
                    '__all__': [_("This article has been deleted")]
                }
            }
            return self.return_error(request, context)

        if Business.delete_article(article):
            return self.return_error(request, {'status': 400})

        context = {'article': article}
        context.update(self.get_context(request, article))

        return self.return_success(request, context)


class ArticleEditView(ArticleBaseView):

    template_name = 'article/article-edit.html'
    template_for_create = 'article/article-create.html'
    form_article = ArticleForm
    the_article = None

    def prepare_context(self, request, context):
        return context

    def prepare_initial_data(self, initial):
        return initial

    def get_temp_article(self, user):
        return Business.create_temp_article(user)

    @method_decorator(login_required)
    def get(self, request, article_id=None, *args, **kwargs):

        article = get_article(article_id)

        self.the_article = article
        # Fail if is not owner
        self.check_is_owner(request, article)

        initial_data = {}

        if not article_id:
            article = None
            #article = self.get_temp_article(request.user)
            #return redirect(reverse('article:edit', args=(article.id,)))
            #return render
            self.template_name = self.template_for_create

        initial_data = self.prepare_initial_data(initial_data)

        form_article = self.form_article(instance=article, author=request.user, initial=initial_data)

        _context = {
            'form_article': form_article,
            'article': article,
        }

        context = self.prepare_context(request, _context)

        return render(request, self.template_name, context)

    @method_decorator(login_required)
    def post(self, request, article_id=None, *args, **kwargs):

        if not article_id:
            article = self.get_temp_article(request.user)
            article_id = article.id
        else:
            article = article = get_article(article_id)

        self.the_article = article

        # Fail if is not owner
        self.check_is_owner(request, article)

        form_article = self.form_article(data=request.POST, files=request.FILES, instance=article, author=request.user)
        form_article.set_author(request.user)

        temp_form = copy.copy(form_article)
        temp_article = copy.copy(article)

        article_saved = form_article.process()

        if article_saved is not False:
            messages.add_message(request, messages.SUCCESS, _('Publicação salva com sucesso'), 'article')
            article_id = form_article.instance.id
            return redirect(reverse('article:edit', args=(article_id,)))
        else:
            messages.add_message(request, messages.ERROR, _('Generic Error'), 'article')

        temp_form.is_valid()
        _context = {'form_article': temp_form, 'article': temp_article}
        return render(request, self.template_name, self.prepare_context(request, _context))
