from django.shortcuts import render
from apps.article import views
from ..forms.article import CoreArticleForm


class CoreArticleEditView(views.ArticleEditView):

    form_article = CoreArticleForm
