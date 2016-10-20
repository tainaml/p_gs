from django.conf import settings
from django.contrib.auth.decorators import login_required
from django.core.cache.utils import make_template_fragment_key
from django.http import JsonResponse, Http404
from django.shortcuts import render
from django.utils.decorators import method_decorator
from django.core.cache import cache
from apps.notifications.service import business as Business
from apps.notifications.service.forms import NotificationForm
from apps.notifications import views

from rede_gsti.settings import NOTIFICATION_ACTIONS


class CoreNotificationIndexView(views.NotificationBaseView):
    template_path = 'notifications/index.html'

    def get(self, request):
        notifications = \
            Business.get_notifications_by_user_and_notification_type_list(
                request.user,
                [settings.SOCIAL_COMMENT, settings.SOCIAL_LIKE, settings.SOCIAL_UNLIKE])

        context = {'notifications': notifications}
        context.update(self.get_context(request))

        return render(request, self.template_path, context)


class CoreNotificationListView(views.NotificationBaseView):
    template_path = 'userprofile/notifications/partials/list-notifications.html'
    form = NotificationForm
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


class CoreNotificationMembersView(views.NotificationBaseView):
    template_path = 'notification/notification-members.html'

    @method_decorator(login_required)
    def get(self, request):
        context = {
            'profile': request.user.profile,
        }

        context.update(self.get_context(request))
        return render(request, self.template_path, context)


class CoreNotificationPollingBase(views.View):

    def set_notification_group(self, notification_type):

        if notification_type not in settings.NOTIFICATION_GROUP.keys():
            raise Exception("There is a group for this type of notifications")

        return settings.NOTIFICATION_GROUP[notification_type]


class CoreNotificationPollingCount(CoreNotificationPollingBase):
    template_path = ''

    @method_decorator(login_required)
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
            visualized=False
        )

        count = notifications.count()
        notifications_id = [n.id for n in notifications]

        context = {
            'count': count,
            'notifications': notifications_id
        }

        return JsonResponse(context, status=200)


class CoreNotificationPollingLoad(CoreNotificationPollingBase):
    template_path = 'notification/partials/navbar/notification-include-list.html'

    @method_decorator(login_required)
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
            visualized=None,
            read=None,
            items_per_page=5,
            page=1
        )

        notifications_id = [n.id for n in notifications]

        response_data = {
            'total': paginator.count,
            'total_unread': notifications.filter(visualized=False).count(),
            'notifications': notifications,
            'notifications_label': NOTIFICATION_ACTIONS,
            'notifications_id': notifications_id,
            'notification_type': notification_type
        }

        context = {
            'notifications': notifications_id,
            'template': render(request, self.template_path, response_data).content
        }

        return JsonResponse(context, status=200)


class CoreNotificationClear(views.NotificationBaseView):

    @method_decorator(login_required)
    def post(self, request):
        notifications_ids = request.POST.getlist('notifications[]')
        notifications = Business.set_notification_as_visualized(notifications_ids)


        status = [Business.NOT_READ, Business.NOT_VISUALIZED, Business.GENERAL]
        notification_types = ["members", "posts", "general"]
        for ntype in notification_types:
            count_key = Business.make_key(request.user, "count_visualized", ntype)
            cache.delete(count_key)

            for stat in status:
                    key = Business.make_key(request.user, stat, ntype)
                    cache.delete(key)

        context = {'notifications': [n.id for n in notifications]}
        context.update(self.get_context(request))

        return JsonResponse(context, status=200)


class CoreNotificationMarkAsRead(views.NotificationBaseView):

    @method_decorator(login_required)
    def post(self, request):
        notifications_ids = request.POST.getlist('notifications[]')
        notifications = Business.set_notification_as_read(notifications_ids)


        context = {
            'notifications': [n.id for n in notifications],
            'status': True if notifications else False
        }
        context.update(self.get_context(request))

        return JsonResponse(context, status=200)


class CoreNotificationMarkAsReadAndVisualized(views.NotificationBaseView):

    @method_decorator(login_required)
    def post(self, request):

        notifications_ids = request.POST.getlist('notifications[]')
        notifications = Business.set_notification_as_read_and_visualized(notifications_ids)

        context = {
            'notifications': [n.id for n in notifications],
            'status': True if notifications else False
        }
        context.update(self.get_context(request))

        return JsonResponse(context, status=200)
