from django.contrib.contenttypes.models import ContentType
from apps.core.business.content_types import ContentTypeCached

from apps.feed.models import FeedObject
from apps.rede_gsti_signals.signals.home import clear_article_cache
from apps.taxonomy.service import business as BusinessTaxonomy
from apps.feed.service import business as BusinessFeed


def save_taxonomies(feed_instance=None, data=None):

    taxs = []
    for item in feed_instance.communities.all():
        taxs.append(item.taxonomy)

    taxonomies = BusinessTaxonomy.save_taxonomies_for_model(feed_instance, taxs)
    return taxonomies


def save_communities(feed_instance=None, data=None):
    temp_communities = data.get('communities', [])
    feed_instance.communities = temp_communities
    feed_instance.save()
    return feed_instance


def delete_communities(feed_instance=None, data=None):
    communities = feed_instance.communities.all()
    for community in communities:
        feed_instance.communities.remove(community)


def delete_taxonomies(feed_instance=None, data=None):
    taxonomies = feed_instance.taxonomies.all()
    for taxonomy in taxonomies:
        feed_instance.taxonomies.remove(taxonomy)


def save_feed_question(question, data=None):
    feed_object = BusinessFeed.feed_get_or_create(question)
    feed_object.save()
    return feed_object


def save_feed_official(feed_object, data=None):
    feed_object.official = data.get('official', False)
    feed_object.save()
    return feed_object


def toggle_feed_official(content_type, object_id):

    content_type = ContentTypeCached.objects.get(model=content_type)
    feed = FeedObject.objects.get(
        content_type=content_type,
        object_id=object_id
    )

    feed.official = not feed.official
    feed.save()

    clear_article_cache.send(sender=feed.__class__, instance=feed, force=True)

    return feed

def user_can_make_as_official(user):
    pass