import json
from django.http import HttpResponse
from django.shortcuts import render
from apps.article import views
from ..forms.article import CoreArticleForm
from ..business import feed as BusinessFeed

class CoreArticleEditView(views.ArticleEditView):

    form_article = CoreArticleForm


class CoreArticleView(views.ArticleView):

    def get_context(self, request, article_instance=None):
        feed_object = BusinessFeed.BusinessFeed.get_feed(article_instance)
        return {
            'feed': feed_object
        }