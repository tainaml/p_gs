from apps.taxonomy.service import business as BusinessTaxonomy
from apps.feed.service import business as BusinessFeed


def save_taxonomies(article_instance=None, data=None):

    taxonomies = BusinessTaxonomy.save_taxonomies_for_model(article_instance, data['taxonomies'])

    return taxonomies

def save_feed_item(article_instance, data=None):
    feed_object = BusinessFeed.feed_get_or_create(article_instance)
    feed_object.save()
    return feed_object



