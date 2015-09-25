from django.shortcuts import render
from django.views.generic import View
from django.utils.translation import ugettext as _
from django.http import Http404

__author__ = 'phillip'


class NotificationBaseView(View):
    not_found = Http404(_('Notifications not Found.'))

    def get_context(self, request=None, instance=None):
        return {}



class NotificationIndexView(NotificationBaseView):

    template_path = 'notifications/index.html'

    def get(self, request):

        context = {}
        context.update(self.get_context(request))

        return render(request, self.template_path, context)