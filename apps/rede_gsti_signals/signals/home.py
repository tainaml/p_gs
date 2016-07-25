import logging
from django.contrib.contenttypes.models import ContentType
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.core.cache import caches

from apps.article.models import Article
from apps.feed.models import FeedObject

logger = logging.getLogger('signals')

cache = caches['default']

@receiver(post_save, sender=FeedObject)
def refresh_home_block(sender, **kwargs):
    logger.info("Refreshing home block...")

    feed_object = kwargs['instance']

    if not feed_object.official or not feed_object.official__old_value:
        return

    article_type = ContentType.objects.get_for_model(Article)
    if feed_object and feed_object.content_object and feed_object.content_type == article_type:

        home_caches = cache.get('home_page_caches')
        if home_caches:
            for home_cache in home_caches:
                cache.delete(home_cache)

        logger.info("Iterating taonomies...")
        for tax in feed_object.taxonomies.all():
            logger.info("    >" + str(tax))


        home_excludes = cache.get('global_home_excludes')
        if home_excludes:
            for home_exclude in home_excludes:
                cache.delete(home_exclude)

        cache.delete('global_home_excludes')