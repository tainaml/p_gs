from django.conf import settings
from django.shortcuts import render
from apps.notifications.service import business as Business

__author__ = 'phillip'
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
