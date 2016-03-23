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


    # key_name = 'home-block-taxonomy'
    # block_keys = [
    #     'home_block_full_width',
    #     'home_block_half_two',
    #     'home_block_half_three',
    #     'home_block_third',
    #     'home_block_highlight',
    #     'home_block_article_home',
    # ]

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

            _home_caches = []

            home_excludes = cache.get('global_home_excludes')
            if home_excludes:
                for home_exclude in home_excludes:
                    _home_caches.append(home_exclude)
                    cache.delete(home_exclude)

            print _home_caches
            cache.delete('global_home_excludes')

            # # Limpando cache que evita duplicata na home.
            # excludes_key = 'home_excludes__%s' % tax.slug.lower()
            # cache.delete(excludes_key)

            # for key_name in block_keys:
            #     logger.info("        >" + key_name)
            #
            #     for _home_cache in _home_caches:
            #
            #         temp_key = '%s-%s-%s' % (
            #             key_name,
            #             _home_cache,
            #             tax.slug.lower()
            #         )
            #
            #         cache.delete(temp_key)