from django.conf import settings
from django.http import JsonResponse, Http404
from django.shortcuts import render

from apps.notifications.service import business as Business
from apps.notifications.views import NotificationBaseView

class CoreNotificationIndexView(NotificationBaseView):
    template_path = 'notifications/index.html'

    def get(self, request):

        notifications = \
        Business.get_notifications_by_user_and_notification_type_list(
            request.user,
            [settings.SOCIAL_COMMENT, settings.SOCIAL_LIKE, settings.SOCIAL_UNLIKE])

        context = {'notifications': notifications}
        context.update(self.get_context(request))

        return render(request, self.template_path, context)


class CoreNotificationMembersView(NotificationBaseView):
    template_path = 'notifications/members.html'

    def get(self, request):

        notifications = \
        Business.get_notifications_by_user_and_notification_type_list(
            request.user,
            [settings.SOCIAL_FOLLOW])

        context = {'notifications': notifications}
        context.update(self.get_context(request))

        return render(request, self.template_path, context)


class CoreNotificationPollingCount(NotificationBaseView):
    template_path = ''

    def set_notification_group(self, notification_type):
        if notification_type == "members":
            notification_group = [settings.SOCIAL_FOLLOW]
        elif notification_type == "comments":
            notification_group = [settings.SOCIAL_COMMENT]
        else:
            notification_group = [settings.SOCIAL_COMMENT, settings.SOCIAL_LIKE, settings.SOCIAL_UNLIKE]

        return notification_group

    def get(self, request, notification_type):

        if not request.is_ajax():
            raise Http404()

        notification_group = self.set_notification_group(notification_type)

        notifications = Business.get_notifications_by_user_and_notification_type_list(
            request.user,
            notification_group
        )

        notifications = notifications.filter(read=False)

        count = notifications.count()
        notifications_id = [n.id for n in notifications]

        context = {
            'count': count,
            'notifications': notifications_id
        }
        context.update(self.get_context(request))

        return JsonResponse(context, status=200)


class CoreNotificationClear(NotificationBaseView):

    def post(self, request):

        notifications_ids = request.POST.getlist('notifications[]')

        notifications = Business.set_notification_as_read(notifications_ids)

        context = {'notifications': [n.id for n in notifications]}
        context.update(self.get_context(request))

        return JsonResponse(context, status=200)