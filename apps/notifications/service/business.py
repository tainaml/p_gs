__author__ = 'phillip'
from django.contrib.contenttypes.models import ContentType
from ..models import Notification
from ..local_exceptions import NotValidNotificationSettings
from django.conf import settings


def get_content_by_object(content_object=None):
    return ContentType.objects.get_for_model(content_object)


def get_model_type(content_type=None):
    model_type = ContentType.objects.get(model=content_type)

    return model_type


def send_notification(author=None, to=None, notification_action=None,
                      target_object=None):
    if not hasattr(settings, 'NOTIFICATION_ACTIONS') or not isinstance(
            notification_action, int):
        raise NotValidNotificationSettings('not_valid_setting',
                                           'NOTIFICATION_ACTIONS')

    notification = Notification(
        author=author,
        to=to,
        notification_action=notification_action,
        target_content_type=get_content_by_object(target_object),
        target_object_id=target_object.id
    )

    notification.save()

    return notification


def send_notification_to_many(author=None, to_list=None,
                              notification_action=None,
                              target_object=None):
    notification_list = []
    if not to_list:
        to_list = []

    for to in to_list:
        notification_list.append(
            send_notification(author, to, notification_action, target_object))

    return notification_list

def get_notifications_by_user_and_notification_type_list(user=None,
                                                         notification_action=None):
    if not notification_action:
        notification_action = []

    notifications = Notification.objects.filter(
        to=user,
        notification_action__in=notification_action
    )

    return notifications