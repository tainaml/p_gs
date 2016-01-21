import logging
from django.contrib.contenttypes.models import ContentType
from django.core.cache.utils import make_template_fragment_key
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.core.cache import cache

from apps.article.models import Article
from apps.feed.models import FeedObject

logger = logging.getLogger('signals')

@receiver(post_save, sender=FeedObject)
def refresh_home_block(sender, **kwargs):
    logger.info("Refreshing home block...")
    key_name = 'home-block-taxonomy'
    block_keys = [
        'home_block_full_width',
        'home_block_half_two',
        'home_block_half_three',
        'home_block_third',
        'home_block_highlight',
        'home_block_article_home',
    ]

    feed_object = kwargs['instance']

    article_type = ContentType.objects.get_for_model(Article)
    if feed_object and feed_object.content_object and feed_object.content_type == article_type:

        logger.info("Iterating taonomies...")
        for tax in feed_object.taxonomies.all():
            logger.info("    >" + str(tax))
            for key_name in block_keys:
                logger.info("        >" + key_name)
                # temp_key = make_template_fragment_key(key_name, (
                #     tax.slug.lower()
                # ))
                # workaround
                temp_key = key_name + "-" + tax.slug.lower()
                cache.delete(temp_key)