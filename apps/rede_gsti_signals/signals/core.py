from django.conf import settings
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.core.cache import cache

from apps.community.models import Community
from apps.comment.models import Comment
from apps.notifications.service import business as Business
from apps.core.business import configuration


@receiver(post_save, sender=Community)
def refresh_footer(sender, **kwargs):
    footer = cache.get("footer")
    if footer:
        cache.delete("footer")


@receiver(post_save, sender=Comment)
def comment_action(sender, **kwargs):
    comment = kwargs['instance']

    if comment:
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
