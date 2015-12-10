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
    saved = article.save()
    return False if saved is False else article

def delete_article(article):
    article.status = article.STATUS_TRASH
    return article.save()

def count_articles(author):
    try:
        count = Article.objects.filter(author=author, status=Article.STATUS_PUBLISH).count()
    except:
        return 0

    return count


def get_articles_by_user(author):
    try:
        articles = Article.objects.get(author=author)
    except Article.DoesNotExist:
        articles = False

    return articles