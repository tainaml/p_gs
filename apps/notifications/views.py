from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from django.utils.decorators import method_decorator
from django.utils.translation import ugettext as _
from django.views.generic import View
from django.http import Http404, JsonResponse, HttpResponse

from apps.notifications.service.forms import NotificationForm
from apps.notifications.service import business as Business

from rede_gsti.settings import NOTIFICATION_ACTIONS, NOTIFICATION_GROUP


class NotificationListBaseView(View):
    xhr = False
    itens_by_page = 10
    context = {}
    response_data = {}
    # form = ListNotificationForm

    @property
    def template_list_path(self):
        raise NotImplementedError(_("you must specify the template_list_path property"))

    def do_process(self, request=None):
        self.response_data['template'] = render(request,
                                                self.template_list_path,
                                                self.context).content

        return render(request, self.template_list_path, self.context)


class NotificationBaseView(View):

    template_path = None
    template_path_partial = 'notification/partials/notifiation-include-segment.html'
    notification_type = None

    form_notification = NotificationForm

    def return_process(self, request, context=None):
        if not context:
            context = []

        if request.is_ajax():
            return self.return_ajax(request, context)

        return render(request, self.template_path, context)

    def return_ajax(self, request, context=None):
        if not context:
            context = []

        # response_data = {'template': render(request, self.template_path_partial, context).content}
        # return JsonResponse(response_data, status=context.get('status', 400))
        return render(request, self.template_path_partial, context)

    def not_found(self, request, context=None):
        if not context:
            context = []

        if request.is_ajax():
            response_data = {'error': context.get('error', None)}
            return JsonResponse(response_data, status=404)

        raise Http404(_('Notification not found!'))

    def get_context(self, request, instance=None):
        return {}

    def set_notification_group(self, notification_type):
        if notification_type not in NOTIFICATION_GROUP.keys():
            raise Exception("There is a group for this type of notifications")

        return NOTIFICATION_GROUP[notification_type]

    @method_decorator(login_required)
    def get(self, request):

        context = dict()

        try:
            notification_group = self.set_notification_group(self.notification_type)
        except Exception as e:
            return self.not_found(request, {'error': e.message})

        form = self.form_notification(request.GET)
        form.set_to_user(request.user)
        form.set_notification_group(notification_group)
        form.set_items_per_page(10)

        notification_object = form.process()

        notifications = notification_object.get('notifications')
        notifications_paginator = notification_object.get('paginator')
        notifications_counter = notification_object.get('all_notifications')

        context['profile'] = request.user.profile
        context['paginator'] = notifications_paginator
        context['notifications'] = notifications
        context['notifications_label'] = NOTIFICATION_ACTIONS
        context['url_pagination'] = 'notifications:%s' % self.notification_type
        context['status'] = 200
        context['page'] = int(form.cleaned_data.get('page')) + int(1)

        return self.return_process(request, context)


class NotificationIndexView(NotificationBaseView):

    template_path = 'notifications/index.html'
    notification_type = []


class NotificationMembersView(NotificationBaseView):

    template_path = 'notification/notification-members.html'
    notification_type = 'members'


class NotificationPostsView(NotificationBaseView):

    template_path = 'notification/notification-posts.html'
    notification_type = 'posts'


class NotificationGeneralsView(NotificationBaseView):

    template_path = 'notification/notification-general.html'
    notification_type = 'general'


class NotificationMarkAllAsRead(NotificationBaseView):

    @staticmethod
    def bad_request():
        raise Http404()

    def return_process(self, request, context=None):
        if 'next' not in context:
            return self.bad_request()

        return redirect(context.get('next'))

    @method_decorator(login_required)
    def post(self, request):

        if 'notification' not in request.POST:
            return self.bad_request()

        if 'url_next' not in request.POST:
            return self.bad_request()

        notification_type = request.POST.get('notification')
        url_next = request.POST.get('url_next')

        notification_group = self.set_notification_group(notification_type)

        notification_object = Business.get_notifications(
            user=request.user,
            notification_actions=notification_group,
            read=False
        )

        notifications = notification_object.get('notifications')

        notifications_read = Business.set_notification_as_read([n.id for n in notifications])

        return self.return_process(request, {
            'notification_type': notification_type,
            'notifications_read': notifications_read,
            'next': url_next
        })


class NotificationMarkAllAsVisualized(NotificationBaseView):

    @staticmethod
    def bad_request():
        raise Http404()

    def return_process(self, request, context=None):
        if 'next' not in context:
            return self.bad_request()

        return redirect(context.get('next'))

    @method_decorator(login_required)
    def post(self, request):

        if 'notification' not in request.POST:
            return self.bad_request()

        if 'url_next' not in request.POST:
            return self.bad_request()

        notification_type = request.POST.get('notification')
        url_next = request.POST.get('url_next')

        notification_group = self.set_notification_group(notification_type)

        notification_object = Business.get_notifications(
            user=request.user,
            notification_actions=notification_group,
            visualized=False
        )

        notifications = notification_object.get('notifications')

        notifications_visualized = Business.set_notification_as_visualized([n.id for n in notifications])

        return self.return_process(request, {
            'notification_type': notification_type,
            'notifications_visualized': notifications_visualized,
            'next': url_next
        })
