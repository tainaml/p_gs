from django.contrib.auth.decorators import login_required, permission_required
from django.http import HttpResponseForbidden, Http404
from django.shortcuts import render, get_object_or_404
from django.utils.translation import gettext as _
from .service import business as Business
from .service.forms import ArticleForm
from django.core.files.uploadedfile import SimpleUploadedFile


@login_required
def article_edit(request, article_slug=None, article_id=None):

    article = Business.get_article(article_id)

    if article_id:
        if not article.id or article.slug != article_slug:
            raise Http404(_('Article not found'))

    #article_form = ArticleForm(data_model=article)
    return render(request, 'article/edit.html', {})


@login_required()
def article_save(request):
    pass
