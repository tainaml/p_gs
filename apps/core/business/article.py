import datetime
from apps.feed.models import FeedObject
from apps.feed.service import business as BusinessFeed
from apps.article.models import Article
from django.db.models import Q
from django.db.models.query import Prefetch
from reversion import revisions as reversion
from apps.temp_comment.models import TempComment
import calendar


def get_article(year=None, month=None, slug=None, prefetch=None):
    """
    This method search for article id and slug.
    If a previous slug found, return the last version of the article with the redirect parameter
    :param article_id:
    :param slug:
    :return:
    """
    article = None
    redirect = False

    try:

        try:
            year = int(year)
            month = int(month)
        except Exception:
            pass

        # article = Article.objects.prefetch_related('old_comments',  "feed")


        if prefetch is None:
            prefetch = ('content_object',)

        feed_article = FeedObject.objects.filter\
            (article__publishin__year=year, article__publishin__month=month, article__slug=slug).prefetch_related(*prefetch).get()

        article = feed_article.content_object
    except FeedObject.DoesNotExist, FeedObject.MultipleObjectsReturned:
        feed_article = None
        try:
            temp_feed_articles = FeedObject.objects.filter(article__publishin__year=year, article__publishin__month=month).prefetch_related(*prefetch)

            #TODO make a better criteria to avoid multiqueries
            for temp__feed_article in temp_feed_articles:
                version_list = reversion.get_for_object(temp__feed_article.content_object).get_unique()
                slug_list = [version.field_dict['slug'] for version in version_list]
                feed_article = temp__feed_article
                if slug in slug_list:
                    article = temp__feed_article.content_object
                    feed_article = temp__feed_article
                    redirect = True
                    break

        except Article.DoesNotExist:
            pass

    return {'article': article, 'redirect': redirect, 'feed': feed_article}

def save_feed_item(article, data=None):
    feed_object = BusinessFeed.feed_get_or_create(article)
    feed_object.date = article.publishin if article.is_published() else None

    for(key, value) in data.items():
        if hasattr(feed_object, key):
            setattr(feed_object, key, value)

    feed_object.save()

    return feed_object


class HomeCache(object):

    def __init__(self):
        pass


class PegadorDeArtigo(object):
    pass


def has_old_comments(article):
    try:
        return TempComment.objects.filter(article=article).exists()
    except TempComment.DoesNotExist:
        return False


