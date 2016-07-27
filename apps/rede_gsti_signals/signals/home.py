import logging
from django.contrib.contenttypes.models import ContentType
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.core.cache import caches

from apps.article.models import Article
from apps.core.cachecontrol import cachecontrol
from apps.core.utils import generate_home_cache_key
from apps.feed.models import FeedObject

logger = logging.getLogger('signals')

cache = caches['default']


@receiver(post_save, sender=FeedObject)
def refresh_home_block(sender, **kwargs):
    logger.info("Refreshing home block...")

    feed_object = kwargs.get('instance', None)

    if not feed_object.official or not feed_object.official__old_value:
        #return
        pass



    article_type = ContentType.objects.get_for_model(Article)
    if feed_object and feed_object.content_object and feed_object.content_type == article_type:

        # try:
        #     home_caches = cache.get('home_page_caches', [])
        #     for home_cache in home_caches:
        #         cache.delete(home_cache)
        #         print 1
        #         # [cache.delete(home_cache) for home_cache in home_caches]
        # except Exception,e:
        #     pass
        #
        # logger.info("Iterating taonomies...")
        # for tax in feed_object.taxonomies.all():
        #     logger.info("    >" + str(tax))
        #
        #
        # home_excludes = cache.get('global_home_excludes', [])
        # for home_exclude in home_excludes:
        #     cache.delete(home_exclude)

        try:

            for community in feed_object.communities.all():
                category_slug = community.taxonomy.slug
                cachecontrol.clear_group('global_home::%s' % category_slug)

            # cachecontrol.clear_group('homes')
            cachecontrol.clear_group('os_excludes')

        except Exception, e:
            print e.message