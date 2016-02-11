from distutils.command.register import register
from django import template

from apps.account.service.business import create_token
from apps.notifications.service import business as Business

from rede_gsti.settings import NOTIFICATION_GROUP, NOTIFICATION_ACTIONS

register = template.Library()


@register.inclusion_tag('notification/templatetags/notification-include-navbar.html', takes_context=True)
def notification_navbar(context, notification_type, count=5):

    request = context['request']

    notification_group = NOTIFICATION_GROUP[notification_type] if notification_type in NOTIFICATION_GROUP.keys() else []

    notifications, paginator = Business.get_notifications(
        user=request.user,
        notification_actions=notification_group,
        read=None,
        items_per_page=5,
        page=1
    )

    notifications_not_read, paginator_not_read = Business.get_notifications(
        user=request.user,
        notification_actions=notification_group,
        read=False
    )

    count = notifications_not_read.count()
    notifications_not_read_id = [n.id for n in notifications_not_read]

    response_data = {
        'request': request,
        'total': paginator.count,
        'count': count,
        'notifications': notifications,
        'notifications_label': NOTIFICATION_ACTIONS,
        'notifications_id': notifications_not_read_id,
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