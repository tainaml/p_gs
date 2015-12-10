from django.conf import settings
from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver
from apps.community.models import Community
from apps.socialactions.models import UserAction, Counter
from apps.article.models import Article
from apps.comment.models import Comment
from apps.core.business import embeditem, configuration
from django.core.cache import cache
from apps.notifications.service import business as Business


@receiver(post_save, sender=UserAction)
def counter_post_save(sender, **kwargs):
    count_user_actions(sender, **kwargs)


@receiver(post_delete, sender=UserAction)
def counter_post_delete(sender, **kwargs):
    count_user_actions(sender, **kwargs)


def count_user_actions(sender, **kwargs):

    action = kwargs['instance']
    if action:
        count = UserAction.objects.filter(object_id=action.object_id,
                content_type=action.content_type,
                action_type = action.action_type,
                target_user=action.target_user).count()

        try:
            counter_instance = Counter.objects.get(object_id=action.object_id,
                    content_type=action.content_type,
                    action_type = action.action_type,
                    target_user=action.target_user)
        except:
            counter_instance= Counter(object_id=action.object_id,
                    content_type=action.content_type,
                    action_type = action.action_type,
                    target_user=action.target_user
                                      )

        counter_instance.count=count
        counter_instance.save()


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
            if configuration.check_config_to_notify(to, action.action_type, action.content_object):
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
                if configuration.check_config_to_notify(to, settings.SOCIAL_COMMENT, comment.content_object):
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