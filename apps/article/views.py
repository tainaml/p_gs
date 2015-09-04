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


class ArticleBaseView(View):

    article_not_found = Http404(_('Article not Found.'))

    def filter_article(self, request, article_id=None):
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


class ArticleView(ArticleBaseView):

    template_name = 'article/view_article.html'

    def get(self, request, article_slug, article_id):
        article = self.filter_article(request, article_id)
        print article.slug
        if not str(article.slug) == str(article_slug):
            raise self.article_not_found

        return render(request, self.template_name, {'article': article})


class ArticleEditView(ArticleBaseView):

    template_name = 'article/edit.html'
    form_article = ArticleForm

    @method_decorator(login_required)
    def get(self, request, article_id=None, *args, **kwargs):

        article = self.filter_article(request, article_id)

        if not article_id:
            article = Business.create_temp_article(request.user)
            return redirect(reverse('article:edit', args=(article.id,)))

        form_article = self.form_article(prefix='article', instance=article)

        return render(request, self.template_name, {'form': form_article})

    @method_decorator(login_required)
    def post(self, request, article_id=None, *args, **kwargs):

        article = self.filter_article(request, article_id)
        form_article = self.form_article(request.POST, request.FILES, prefix='article', instance=article)
        form_article.set_author(request.user)

        article_saved = form_article.process()
        if article_saved is not False:
            messages.add_message(request, messages.SUCCESS, _('Success'))
            article_id = form_article.instance.id
            return redirect(reverse('article:edit', args=(article_id,)))
        else:
            print 'erro'

        return render(request, self.template_name, {'form': form_article})