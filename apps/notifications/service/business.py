from django.db.models import Q
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
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
                                                         notification_actions=None,
                                                         items_per_page=None, page=None):
    if not notification_actions:
        notification_actions = []

    notifications = Notification.objects.filter(
        to=user,
        notification_action__in=notification_actions
    ).order_by("-notification_date")

    items_per_page = items_per_page if items_per_page else 10

    paginated_notifications = Paginator(notifications, items_per_page)

    try:
        paginated_notifications = paginated_notifications.page(page)
    except PageNotAnInteger:
        paginated_notifications = paginated_notifications.page(1)
    except EmptyPage:
        paginated_notifications = []

    return paginated_notifications


def get_notifications(user=None, notification_actions=None, visualized=None, read=None, items_per_page=None, page=None):
    if not notification_actions:
        notification_actions = []

    criteria = (Q(to=user) & Q(notification_action__in=notification_actions))

    if visualized is not None:
        criteria &= Q(visualized=visualized)

    if read is not None:
        criteria &= Q(read=read)

    notifications = Notification.objects.filter(criteria).order_by("-notification_date")

    paginator = False

    if items_per_page and page:
        items_per_page = items_per_page if items_per_page else 10
        paginator = Paginator(notifications, items_per_page)

        try:
            notifications = paginator.page(page)
        except PageNotAnInteger:
            notifications = paginator.page(1)
        except EmptyPage:
            notifications = []

    return notifications, paginator


def set_notification_as_read(notifications_ids):
    notifications_read = []

    notifications = Notification.objects.filter(id__in=notifications_ids)

    for n in notifications:
        n.read = True
        n.save(update_fields=['read'])
        notifications_read.append(n)

    return notifications_read


def set_notification_as_visualized(notifications_ids):
    notifications_visualized = []
    notifications = Notification.objects.filter(id__in=notifications_ids)

    for n in notifications:
        n.visualized = True
        n.save(update_fields=['visualized'])
        notifications_visualized.append(n)

    return notifications_visualized


def token_is_valid(request):
    token = request.GET.get('token', False)
    token_session = request.session.get('token', False)

    if not token:
        raise Exception('Token is not defined!')

    if token_session and (token != token_session):
        raise Exception('Token is not valid!')

    return True
