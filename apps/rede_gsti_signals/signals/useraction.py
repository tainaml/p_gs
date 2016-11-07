from django.db.models import Model
from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver
from apps.core.tasks import count_user_actions
from apps.socialactions.models import UserAction
from apps.article.models import Article
from apps.core.business import embeditem
from apps.notifications.service import business as Business


@receiver(post_save, sender=UserAction)
def counter_post_save(sender, **kwargs):
    action = kwargs['instance']
    if action:
        count_user_actions.delay(action)


@receiver(post_delete, sender=UserAction)
def counter_post_delete(sender, **kwargs):
    action = kwargs['instance']
    if action:
        count_user_actions.delay(action)



@receiver(post_save, sender=UserAction)
def social_action(sender, **kwargs):
    action = kwargs['instance']

    _action_type = None

    if action:
        author = action.author
        to = action.target_user

        allowed_content_type = [
            'comment',
            'article',
            'question',
            'answer'
        ]

        not_allowed_content_type = [
            'community'
        ]

        if action.content_type.model in allowed_content_type and action.content_object and not to:
            to = action.content_object.author

        elif action.content_type.model in ['user'] and not to:
            to = action.content_object

        _action_type = action.action_type
        if not isinstance(_action_type, Model) and isinstance(action.content_object, Model):
            _action_type = action.content_object

        if action.content_type.model not in not_allowed_content_type and to != author:
            Business.send_notification(
                author=action.author,
                to=to,
                notification_action=action.action_type,
                target_object=action.content_object
            )


@receiver(post_save, sender=Article)
def article_action(sender, **kwargs):

    instance = kwargs['instance'] if 'instance' in kwargs else False
    if not instance:
        return

    embeds = embeditem.EmbedBusiness(instance)
    embeds.save()
