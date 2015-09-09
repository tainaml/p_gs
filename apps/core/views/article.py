from django.shortcuts import render
from apps.article import views
from ..forms.article import CoreArticleForm, CoreArticleCategoriesForm


class CoreArticleEditView(views.ArticleEditView):

    form_article = CoreArticleForm