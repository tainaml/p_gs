from django.conf import settings
from django.http import JsonResponse, Http404
from django.shortcuts import render

from apps.notifications.service import business as Business
from apps.notifications.service.forms import ListNotificationForm
from rede_gsti.settings import NOTIFICATION_ACTIONS

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


class CoreNotificationListView(NotificationBaseView):
    template_path = 'userprofile/notifications/partials/list-notifications.html'
    form = ListNotificationForm
    notification_actions = settings.NOTIFICATION_ACTIONS.keys()
    itens_per_page = 10

    def get(self, request):
        form = self.form(
            user=request.user,
            notification_actions=self.notification_actions,
            itens_by_page=self.itens_per_page,
            data=request.GET
        )

        notifications = form.process()

        context = {
            'notifications': notifications,
            'profile': request.user.profile,
            'form': form,
            'page': form.cleaned_data['page'] + 1
        }
        context.update(self.get_context(request))

        return render(request, self.template_path, context)


class CoreNotificationMemberListView(CoreNotificationListView):
    template_path = 'userprofile/notifications/partials/list-notifications.html'
    notification_actions = [settings.SOCIAL_FOLLOW, settings.SOCIAL_LIKE]


class CoreAnswersAndCommentsListView(CoreNotificationListView):
    template_path = 'userprofile/notifications/partials/list-notifications.html'
    notification_actions = [settings.SOCIAL_FOLLOW]


class CoreNotificationMembersView(NotificationBaseView):
    template_path = 'userprofile/notifications/notifications-members.html'

    def get(self, request):
        context = {
            'profile': request.user.profile,
        }

        context.update(self.get_context(request))
        return render(request, self.template_path, context)


class CoreNotificationPollingBase(NotificationBaseView):

    def set_notification_group(self, notification_type):

        if notification_type not in settings.NOTIFICATION_GROUP.keys():
            raise Exception("There is a group for this type of notifications")

        return settings.NOTIFICATION_GROUP[notification_type]


class CoreNotificationPollingCount(CoreNotificationPollingBase):
    template_path = ''

    def get(self, request, notification_type):

        if not request.is_ajax():
            raise Http404()

        try:
            Business.token_is_valid(request)
        except Exception, e:
            return JsonResponse({'error': e.message, 'status': 400}, status=400)

        notification_group = self.set_notification_group(notification_type)

        notifications, paginator = Business.get_notifications(
            user=request.user,
            notification_actions=notification_group,
            read=False
        )

        count = notifications.count()
        notifications_id = [n.id for n in notifications]

        context = {
            'count': count,
            'notifications': notifications_id
        }
        context.update(self.get_context(request))

        return JsonResponse(context, status=200)


class CoreNotificationPollingLoad(CoreNotificationPollingBase):
    template_path = 'notification/partials/navbar/notification-include-list.html'

    def get(self, request, notification_type):

        if not request.is_ajax():
            raise Http404()

        try:
            Business.token_is_valid(request)
        except Exception, e:
            return JsonResponse({'error': e.message, 'status': 400}, status=400)

        notification_group = self.set_notification_group(notification_type)

        notifications, paginator = Business.get_notifications(
            user=request.user,
            notification_actions=notification_group,
            read=None,
            items_per_page=5,
            page=1
        )

        notifications_id = [n.id for n in notifications]

        response_data = {
            'total': paginator.count,
            'notifications': notifications,
            'notifications_label': NOTIFICATION_ACTIONS,
            'notifications_id': notifications_id,
            'notification_type': notification_type
        }

        context = {
            'notifications': notifications_id,
            'template': render(request, self.template_path, response_data).content
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
