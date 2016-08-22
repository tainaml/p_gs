from apps.feed.service import business as BusinessFeed
from apps.article.models import Article
from reversion import revisions as reversion

def get_article(year=None, month=None, slug=None):
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
        article = Article.objects.get(publishin__year=year, publishin__month=month, slug=slug)

    except Article.DoesNotExist:
        try:
            temp_articles = Article.objects.filter(publishin__year=year, publishin__month=month)
            for temp_article in temp_articles:
                version_list = reversion.get_for_object(temp_article).get_unique()
                slug_list = [version.field_dict['slug'] for version in version_list]
                if slug in slug_list:
                    article = temp_article
                    redirect = True

        except Article.DoesNotExist:
            pass

    return {'article': article, 'redirect': redirect}

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