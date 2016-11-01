from django.db.models.signals import post_save
from django.dispatch import receiver
from apps.comment.models import Comment
from django.conf import settings
from apps.core.business.content_types import ContentTypeCached
from apps.socialactions.models import Counter


def __get_comment_count(content_object):
    content_type = ContentTypeCached.objects.get_for_model(content_object)
    return Comment.objects.filter(
                    content_type=content_type,
                    object_id=content_object.id
                ).count()


@receiver(post_save, sender=Comment)
def comment_count_action(sender, **kwargs):
    """

    Change comment count for content object

    :param sender: Signal required
    :param kwargs: Signal arguments
    :return: Embed Item (saved)
    """

    instance = kwargs['instance'] if 'instance' in kwargs else False
    if not instance:
        return

    comment_count = __get_comment_count(instance.content_object)
    try:

        counter = Counter.objects.defer("count").get(
                action_type=settings.SOCIAL_COMMENT,
                object_id=instance.object_id,
                content_type=instance.content_type

            )
        counter.count = comment_count
        counter.save()

    except Counter.DoesNotExist:
        counter = Counter(
            action_type=settings.SOCIAL_COMMENT,
            object_id=instance.object_id,
            content_type=instance.content_type,
            count=comment_count

        )
        counter.save()
