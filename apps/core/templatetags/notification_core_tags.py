from django import template
from django.conf import settings
from apps.account.service.business import create_token
from apps.notifications.service import business as Business
from apps.notifications.service.business import get_notification_cached, make_key, get_count_notification_cached

register = template.Library()



@register.inclusion_tag('notification/templatetags/notification-include-navbar.html', takes_context=True)
def notification_navbar(context, notification_type, count=5):

    request = context['request']

    NOTIFICATION_GROUP = getattr(settings, 'NOTIFICATION_GROUP', {})
    NOTIFICATION_ACTIONS = getattr(settings, 'NOTIFICATION_ACTIONS', {})

    notification_group = NOTIFICATION_GROUP[notification_type] if notification_type in NOTIFICATION_GROUP.keys() else []

    attribute_key = make_key(request.user, Business.GENERAL, notification_type)
    notifications, paginator = get_notification_cached(attribute_key, user=request.user,
                                                       notification_actions=notification_group,
                                                       visualized=None, items_per_page=5, page=1)


    attribute_key_not_visualized = make_key(request.user, Business.NOT_VISUALIZED, notification_type)
    notifications_not_visualized, paginator_not_visualized  = get_notification_cached(attribute_key_not_visualized, user=request.user,
                                                    notification_actions=notification_group,
                                                    visualized=False)

    attribute_key_not_read = make_key(request.user, Business.NOT_READ, notification_type)
    notifications_not_read, paginator_not_read = get_notification_cached(attribute_key_not_read, user=request.user,
                            notification_actions=notification_group, read=False)


    count_key = make_key(request.user, "count_visualized", notification_type)
    count = get_count_notification_cached(count_key, notifications_not_visualized)

    notifications_not_visualized_id = [n.id for n in notifications_not_visualized]

    response_data = {
        'request': request,
        'total': notifications_not_read.count,
        'count': count,
        'notifications': notifications,
        'notifications_label': NOTIFICATION_ACTIONS,
        'notifications_id': notifications_not_visualized_id,
        'notification_type': notification_type
    }


    return response_data


@register.simple_tag(takes_context=True)
def notification_token(context):
    request = context['request']
    token = request.session.get('token', False)

    if not token:
        token = create_token(request.user)
        request.session['token'] = token

    return token
