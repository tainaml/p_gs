from apps.taxonomy.service import business as BusinessTaxonomy
from apps.feed.service import business as BusinessFeed


def save_taxonomies(instance=None, data=None):
    taxonomies = BusinessTaxonomy.save_taxonomies_for_model(instance, data['taxonomies'])
    return taxonomies

def save_feed_item(instance, data=None):
    feed_object = BusinessFeed.feed_get_or_create(instance)
    feed_object.date = instance.question_date
    feed_object.save()
    return feed_object