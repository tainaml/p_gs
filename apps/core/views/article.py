from django.shortcuts import render
from apps.article.views import ArticleEditView
from ..forms.article import CoreArticleForm

class CoreArticleEditView(ArticleEditView):

    form_article = CoreArticleForm