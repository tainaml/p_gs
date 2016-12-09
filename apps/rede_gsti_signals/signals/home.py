import logging
from django.contrib.contenttypes.models import ContentType
from django.db.models.signals import post_save
from django.dispatch import receiver
from apps.article.models import Article
from apps.core.business.content_types import ContentTypeCached
from apps.core.cachecontrol import cachecontrol
from apps.core.templatetags.article_blocks import ArticleCacheExcludes
from apps.feed.models import FeedObject
import django.dispatch
from django.core.cache import cache

logger = logging.getLogger('signals')

clear_article_cache = django.dispatch.Signal(providing_args=["instance"])


@receiver(clear_article_cache, sender=FeedObject)
def refresh_home_block(sender, **kwargs):

    feed_object = kwargs.get('instance', None)

    force_update = kwargs.get('force', False)

    logger.info("Refreshing home block...")

    __key = 'gsti__excludes__cache__%s'

    print('is_official %s' % feed_object.official)
    print('is old official %s' % feed_object.official__old_value)

    if force_update == False and feed_object.official == False and feed_object.official__old_value == False:
        return

    article_type = ContentTypeCached.objects.get(model='article')
    if feed_object and feed_object.content_object and feed_object.content_type == article_type:

        try:

            cache.delete('HOME::GROUP::%s' % 'home')
            cache.delete('gsti|excludes|%s' % 'home')

            for f in feed_object.communities.all():
                _slug = f.taxonomy.parent.slug
                cache.delete('HOME::GROUP::%s' % _slug)
                cache.delete('gsti|excludes|%s' % _slug)

            # ArticleCacheExcludes.clear('home')
            # cache.delete('HOME_EXCLUDES|||home')
            # cachecontrol.clear_group('global_home::home')
            #
            # cache.delete('gsti__excludes__cache__home')
            #
            # print('Deleting %s' % 'gsti__excludes__cache__home')
            #
            # print "QTDE %d" % feed_object.communities.all().count()
            #
            # for f in feed_object.communities.all():
            #     _slug = f.taxonomy.slug
            #     print _slug
            #     ArticleCacheExcludes.clear(_slug)
            #     cache.delete(__key % _slug)
            #     cache.delete('HOME_EXCLUDES|||%s' % _slug)
            #     # cachecontrol.clear_group('global_home::%s' % _slug)

        except Exception, e:
            pass