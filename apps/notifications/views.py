from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from django.utils.decorators import method_decorator
from django.utils.translation import ugettext as _
from django.views.generic import View
from django.http import Http404, JsonResponse

from apps.notifications.service.forms import NotificationForm

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
    notification_type = None

    form_notification = NotificationForm

    def return_process(self, request, context=None):
        if not context:
            context = []

        if request.is_ajax():
            response_data = {'template': render(request, self.template_path, context).content}
            return JsonResponse(response_data, status=context.get('status', False))

        return render(request, self.template_path, context)

    def not_found(self, request, context=None):
        if not context:
            context = []

        if request.is_ajax():
            response_data = {'error': context.get('error', None)}
            return JsonResponse(response_data, status=404)

        return Http404(_('Notification not found!'))

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
        except Exception, e:
            return self.not_found(request, {'error': e.message})

        form = self.form_notification(2, request.GET)
        form.set_to_user(request.user)
        form.set_notification_group(notification_group)

        notifications, paginator = form.process()

        context['profile'] = request.user.profile
        context['paginator'] = paginator
        context['notifications'] = notifications
        context['notifications_label'] = NOTIFICATION_ACTIONS

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
