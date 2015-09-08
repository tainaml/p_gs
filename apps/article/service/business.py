from django.conf import settings
from django.forms import model_to_dict
from ..models import Article, models
from forms import ArticleForm


def get_article(article_id=None):

    article = Article()

    if article_id:
        try:
            article = Article.objects.get(pk=article_id)
        except Article.DoesNotExist:
            return False

    return article


def create_temp_article(author):
    article = Article()
    article.author = author
    article.status = Article.STATUS_TEMP
    article.save()
    return article


def save_article(article, data):
    return article.save()


def delete_article(article):
    article.status = article.STATUS_TRASH
    return article.save()