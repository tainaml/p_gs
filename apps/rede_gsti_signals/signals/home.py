from django.contrib.contenttypes.models import ContentType
from django.db.models.signals import post_save
from django.dispatch import receiver
from apps.article.models import Article
from apps.community.models import Community
from django.core.cache import cache
from apps.feed.models import FeedObject

"""
@receiver(post_save, sender=Community)
def refresh_footer(sender, **kwargs):
    footer = cache.get("footer")
    if footer:
        cache.delete("footer")
"""

@receiver(post_save, sender=Article)
def refresh_home_block(sender, **kwargs):
    key_name = 'home-block-taxonomy'

    print key_name

    instance = kwargs['instance'] if 'instance' in kwargs else False
    if not instance:
        # Cancel signal if not exists article instance
        print 'dont have instance'
        return

    article_type = ContentType.objects.get_for_model(Article)

    feed_object = None

    try:
        feed_object = FeedObject.objects.get(object_id=instance.pk, content_type=article_type)
    except FeedObject.DoesNotExist, e:
        print e.message

    raise FeedObject.DoesNotExist

    #print feed_object
