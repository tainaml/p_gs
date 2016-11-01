from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver
from apps.core.business.content_types import ContentTypeCached
from apps.socialactions.models import Counter, UserAction


def __get_useraction_count(content_object=None, action_type=None):
    content_type = ContentTypeCached.objects.get_for_model(content_object)
    print "here"
    return UserAction.objects.filter(
                    content_type=content_type,
                    object_id=content_object.id,
                    action_type=action_type
                ).count()

def refresh_useraction_counter(instance):
    useraction_count = __get_useraction_count(instance.content_object, instance.action_type)
    try:

        counter = Counter.objects.defer("count").get(
                action_type=instance.action_type,
                object_id=instance.object_id,
                content_type=instance.content_type

            )
        counter.count = useraction_count
        counter.save()

    except Counter.DoesNotExist:
        counter = Counter(
            action_type=instance.action_type,
            object_id=instance.object_id,
            content_type=instance.content_type,
            count=useraction_count

        )
        counter.save()


@receiver(post_save, sender=UserAction)
def useraction_count_action(sender, **kwargs):
    """

    Change useraction count for content object

    :param sender: Signal required
    :param kwargs: Signal arguments
    :return: Embed Item (saved)
    """

    instance = kwargs['instance'] if 'instance' in kwargs else False
    if not instance:
        return

    refresh_useraction_counter(instance)\

@receiver(post_delete, sender=UserAction)
def useraction_count_action(sender, **kwargs):
    """

    Change useraction count for content object

    :param sender: Signal required
    :param kwargs: Signal arguments
    :return: Embed Item (saved)
    """
    print "here delete"
    instance = kwargs['instance'] if 'instance' in kwargs else False
    if not instance:
        return

    refresh_useraction_counter(instance)
