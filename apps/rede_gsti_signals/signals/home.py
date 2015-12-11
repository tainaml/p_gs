from django.contrib.contenttypes.models import ContentType
from django.core.cache.utils import make_template_fragment_key
from django.db.models.signals import post_save
from django.dispatch import receiver
from apps.article.models import Article
from django.core.cache import cache
from apps.feed.models import FeedObject

@receiver(post_save, sender=Article)
def refresh_home_block(sender, **kwargs):
    key_name = 'home-block-taxonomy'
    block_keys = [
        'home_block_full_width',
        'home_block_half_two',
        'home_block_half_three',
        'home_block_third',
        'home_block_highlight',
        'home_block_article_home',
    ]

    instance = kwargs['instance'] if 'instance' in kwargs else False
    if not instance:
        # Cancel signal if not exists article instance
        print 'dont have instance or is not publish'
        return

    article_type = ContentType.objects.get_for_model(Article)

    feed_object = None
    feed_item = instance.feed

    try:
        feed_object = FeedObject.objects.get(object_id=instance.pk, content_type=article_type)
    except FeedObject.DoesNotExist, e:
        print 'Erro: %s' % e.message
        return

    for tax in feed_object.taxonomies.all():

        for key_name in block_keys:

            temp_key = make_template_fragment_key(key_name, (
                tax.slug.lower()
            ))

            cache.delete(temp_key)