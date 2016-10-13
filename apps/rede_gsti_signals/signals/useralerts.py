from django.conf import settings
from django.contrib.auth import get_user_model
from django.db.models.signals import m2m_changed
from django.dispatch import receiver
from apps.useralerts.models import UserAlert
from apps.notifications.service import business as Business


def alert_send(sender, **kwargs):

    instance = kwargs['instance'] if 'instance' in kwargs else False
    pk_set = kwargs['pk_set'] if 'pk_set' in kwargs else False
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
        users = author_class.objects.filter(id__in=pk_set)

        Business.send_notification_to_many(
            author=author,
            to_list=users,
            target_object=instance,
            notification_action=getattr(settings, 'NOTIFICATION_USERALERT')
        )

    except Exception as e:
        pass


m2m_changed.connect(alert_send, sender=UserAlert.users.through)


