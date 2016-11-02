from django.db.models import Model
from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver
from django.conf import settings
from apps.socialactions.models import UserAction, Counter, UserActionCounter
from apps.article.models import Article
from apps.core.business import embeditem, configuration
from apps.notifications.service import business as Business


@receiver(post_save, sender=UserAction)
def counter_post_save(sender, **kwargs):
    action = kwargs['instance']
    if action:
        count_user_actions(action)


@receiver(post_delete, sender=UserAction)
def counter_post_delete(sender, **kwargs):
    action = kwargs['instance']
    if action:
        count_user_actions(action)

def count_for_field(instance):
    pass

def count_user_actions(action=None):

    count = UserAction.objects.filter(object_id=action.object_id,
                                          content_type=action.content_type,
                                          action_type=action.action_type,
                                          target_user=action.target_user).count()

    #TODO REFACTOR TO A BETTER APROACH
    if action.action_type == settings.SOCIAL_LIKE:
        action.content_object.like_count = count
        action.content_object.save()
    elif action.action_type == settings.SOCIAL_UNLIKE:
        action.content_object.dislike_count = count
        action.content_object.save()
    elif action.action_type == settings.SOCIAL_COMMENT:
        action.content_object.comment_count = count
        action.content_object.save()
    else:

        count = UserAction.objects.filter(object_id=action.object_id,
                                          content_type=action.content_type,
                                          action_type=action.action_type,
                                          target_user=action.target_user).count()

        count_user = UserAction.objects.filter(action_type=action.action_type,
                                               author=action.author).count()
        try:
            counter_instance = Counter.objects.get(object_id=action.object_id,
                                                   content_type=action.content_type,
                                                   action_type=action.action_type,
                                                   target_user=action.target_user)

        except Counter.DoesNotExist:
            counter_instance = Counter(object_id=action.object_id,
                                       content_type=action.content_type,
                                       action_type=action.action_type,
                                       target_user=action.target_user)

        try:
            counter_user_instance = UserActionCounter.objects.get(action_type=action.action_type,
                                                                  author=action.author)
        except UserActionCounter.DoesNotExist:

            counter_user_instance = UserActionCounter(author=action.author, action_type=action.action_type)

        counter_instance.count=count
        counter_instance.save()
        counter_user_instance.count = count_user
        counter_user_instance.save()


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
