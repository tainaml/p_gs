from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver
from apps.socialactions.models import UserAction, Counter
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
