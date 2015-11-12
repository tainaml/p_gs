from django.conf import settings
from django.db.models.signals import post_save
from django.dispatch import receiver
from apps.community.models import Community
from apps.socialactions.models import UserAction
from apps.article.models import Article
from apps.comment.models import Comment
from apps.core.business import embeditem
from django.core.cache import cache
from apps.notifications.service import business as Business

@receiver(post_save, sender=Community)
def refresh_footer(sender, **kwargs):
    footer = cache.get("footer")
    if footer:
        cache.delete("footer")


@receiver(post_save, sender=UserAction)
def social_action(sender, **kwargs):
    action = kwargs['instance']

    if action:
        author = action.author
        to = None

        allowed_content_type = [
            'comment',
            'article',
            'question',
            'answer'
        ]

        not_allowed_content_type = [
            'community'
        ]

        if action.content_type.model in allowed_content_type:
            to = action.content_object.author

        elif action.content_type.model in ['user']:
            to = action.content_object

        if action.content_type.model not in not_allowed_content_type and to != author:
            Business.send_notification(
                author=action.author,
                to=to,
                notification_action=action.action_type,
                target_object=action.content_object
            )


@receiver(post_save, sender=Comment)
def comment_action(sender, **kwargs):
    comment = kwargs['instance']

    if comment:
        if comment.content_type.model in [
            'article',
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


@receiver(post_save, sender=Article)
def article_action(sender, **kwargs):

    instance = kwargs['instance'] if 'instance' in kwargs else False
    if not instance:
        return

    embeds = embeditem.EmbedBusiness(instance)
    embeds.save()