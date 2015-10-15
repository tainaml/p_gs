from apps.taxonomy.service import business as BusinessTaxonomy
from apps.feed.service import business as BusinessFeed
from apps.article.service import business as BusinessArticle


def save_taxonomies(feed_instance=None, data=None):
    taxonomies = BusinessTaxonomy.save_taxonomies_for_model(feed_instance, data['taxonomies'])
    return taxonomies


def save_communities(article_instance=None, data=None):
    pass


def save_feed_item(article, data=None):
    feed_object = BusinessFeed.feed_get_or_create(article)
    feed_object.date = article.publishin if article.is_published() else None
    feed_object.save()
    return feed_object