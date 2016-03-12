from django.conf import settings
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.core.cache import cache
from apps.community.models import Community
from apps.comment.models import Comment
from apps.notifications.service import business as Business
from apps.core.business import configuration
import logging

logger = logging.getLogger('signals')

@receiver(post_save, sender=Community)
def refresh_footer(sender, **kwargs):
    logger.info("Checking Footer cache")
    footer = cache.get("categories")

    if footer:
        logger.info("Footer cache found, cleaning Footer cache.")
        cache.delete("categories")


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
                if configuration.check_config_to_notify(to, settings.SOCIAL_COMMENT, comment.content_object):
                    Business.send_notification(
                        author=author,
                        to=to,
                        notification_action=settings.SOCIAL_COMMENT,
                        target_object=comment.content_object
                    )
