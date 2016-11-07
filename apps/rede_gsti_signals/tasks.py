from ..socialactions.models import UserAction, Counter, UserActionCounter
from rede_gsti.celery import app
from django.conf import settings

@app.task
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
