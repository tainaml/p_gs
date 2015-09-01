from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.core.urlresolvers import reverse
from django.http import Http404, HttpResponseForbidden
from django.shortcuts import render, redirect
from django.utils.decorators import method_decorator
from django.utils.translation import gettext as _
from django.views.generic import View
from .service import business as Business
from .service.forms import ArticleForm


class ArticleEditView(View):

    template_name = 'article/edit.html'
    form_class = ArticleForm
    article_not_found = Http404('Article not Found.')

    def __filter_article(self, request, article_id=None):
        article = Business.get_article(article_id)

        if not article:
            '''
            Only works when article exists
            '''
            raise self.article_not_found

        if article.id and article.author != request.user :
            '''
            Only the article author has permission to edit article
            '''
            return HttpResponseForbidden(_('Operation not permitted'))

        return article

    @method_decorator(login_required)
    def get(self, request, article_id=None, article_slug=None, *args, **kwargs):

        article = self.__filter_article(request, article_id)

        if article_id and (not article.id or article.slug != article_slug):
            '''
            The article slug is not equals
            '''
            raise self.article_not_found

        form_article = ArticleForm(prefix='article', instance=article)

        return render(request, self.template_name, {'form': form_article})

    @method_decorator(login_required)
    def post(self, request, article_id=None, article_slug=None, *args, **kwargs):

        article = self.__filter_article(request, article_id)
        form_article = ArticleForm(request.POST, request.FILES, prefix='article', instance=article)
        form_article.set_author(request.user)

        article_saved = form_article.process()
        if article_saved is not False:
            print 'save with success'
            messages.add_message(request, messages.SUCCESS, _('Success'))
            article_slug = form_article.instance.slug
            article_id = form_article.instance.id
            return redirect(reverse('article:edit', args=(article_slug, article_id,)))
        else:
            print 'erro'

        return render(request, self.template_name, {'form': form_article})