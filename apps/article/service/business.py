from django.conf import settings
from ..models import Article


def save_article():
    pass


def get_article(article_id=None):

    article = Article()

    if article_id:

        try:
            article = Article.objects.get(pk=article_id)
        except Article.DoesNotExist:
            pass

    return article