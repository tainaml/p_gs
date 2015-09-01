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


def save_article(article, data):

    if article.status == Article.STATUS_PUBLISH:
        '''
        if to be publish
        '''
        print 'Status: ' + str(article.status)
        pass

    print 'Article: '
    print model_to_dict(article)

    return article if article.save() else False


