from django.contrib.contenttypes.models import ContentType
from apps.community.models import Community
from apps.taxonomy.service import business as BusinessTaxonomy
from apps.feed.service import business as BusinessFeed
from apps.article.service import business as BusinessArticle
from apps.socialactions.service import business as BusinessSocialActions
from rede_gsti import settings


def save_feed_item(article, data=None):
    feed_object = BusinessFeed.feed_get_or_create(article)
    feed_object.date = article.publishin if article.is_published() else None
    feed_object.save()
    return feed_object
