from django.conf import settings
from django.contrib.auth import get_user_model
from django.db.models.signals import post_save
from django.dispatch import receiver
from apps.useralerts.models import UserAlert
from apps.notifications.service import business as Business


@receiver(post_save, sender=UserAlert)
def alert_send(sender, **kwargs):

    instance = kwargs['instance'] if 'instance' in kwargs else False
    if not instance:
        # Exit if not have instance
        return

    if instance.status != UserAlert.STATUS_PUBLISH:
        # Exit if is not publish
        return

    instance.status = UserAlert.STATUS_SENDED
    instance.save()

    try:
        author_id = getattr(settings, 'NOTIFICATION_ALERT_DEFAULT_AUTHOR')
        author_class = get_user_model()
        author = author_class.objects.get(id=author_id)

        Business.send_notification_to_many(
            author=author,
            to_list=instance.users.all(),
            target_object=instance,
            notification_action=getattr(settings, 'NOTIFICATION_USERALERT')
        )
    except Exception, e:
        pass



