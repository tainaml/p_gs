from django.conf import settings
from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver
from django.core.cache import cache
from apps.community.models import Community
from apps.comment.models import Comment
from apps.notifications.service import business as Business
from apps.core.business import configuration
import logging

logger = logging.getLogger('signals')


def __invalidate_footer_cache__():
    logger.info("Checking Footer cache")
    footer = cache.get("categories")

    if footer:
        logger.info("Footer cache found, cleaning Footer cache.")
        cache.delete("categories")

def __invalidate_cache_community__(**kwargs):
    community = kwargs.get('instance')
    key = "community_%s" % community.slug
    cache.delete(key)


@receiver(post_save, sender=Community)
def refresh_footer(sender, **kwargs):

    __invalidate_cache_community__(**kwargs)
    __invalidate_footer_cache__()


@receiver(post_delete, sender=Community)
def refresh_delete(sender, **kwargs):
    __invalidate_cache_community__(**kwargs)
    __invalidate_footer_cache__()


@receiver(post_save, sender=Comment)
def comment_action(sender, **kwargs):
    comment = kwargs.get('instance')
    created = kwargs.get('created')

    if comment and created:
        if comment.content_type.model in [
            'article',
            'answer',
            'comment'
        ]:
            to = comment.content_object.author
            author = comment.author
            if to != author:
                Business.send_notification(
                    author=author,
                    to=to,
                    notification_action=settings.SOCIAL_COMMENT,
                    target_object=comment.content_object
                )
