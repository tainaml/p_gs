from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.shortcuts import render, redirect
from django.utils.decorators import method_decorator
from django.utils.translation import ugettext as _
from django.views.generic import View
from apps.core.forms.account import CoreDeactivateAccountForm

from apps.core.forms.configuration import ConfigNotificationsForm
from ..business import configuration as BusinessConfig


class CoreSettingsBaseView(View):

    template_path = ""

    def return_success(self, request, context=None):
        return render(request, self.template_path, context)


class CoreSettingsAccountView(CoreSettingsBaseView):

    template_path = "configuration/configuration-account.html"

    @method_decorator(login_required)
    def get(self, request):

        context = {'profile': request.user.profile}

        return self.return_success(request, context)


class CoreSettingsNotificationView(CoreSettingsBaseView):

    template_path = "configuration/configuration-notification.html"
    template_message_successfully = "configuration/partials/modal/message-successfully.html"

    form = ConfigNotificationsForm

    @method_decorator(login_required)
    def get(self, request):

        configurations = BusinessConfig.get_system_configs('notification')
        configurations_obj = BusinessConfig.get_configs(request.user, 'notification')
        configs = {}

        for config in configurations_obj:
            configs[config.key.key] = config.value

        context = {
            'profile': request.user.profile,
            'configurations': configurations,
            'configs': configs,
            'configs_obj': configurations_obj
        }

        return self.return_success(request, context)

    @method_decorator(login_required)
    def post(self, request):

        form = self.form(request.POST)
        form.set_entity(request.user)

        if form.process():
            context = {
                # Translators:
                "title": _("Configuration Notification"),
                "message": _("Your settings have been successfully changed!")
            }

            return JsonResponse({
                'template': render(request, self.template_message_successfully, context).content
            }, status=200)

        return JsonResponse({'errors': form.errors}, status=400)


class CoreDeactivateAccountView(CoreSettingsBaseView):

    template_path = "configuration/configuration-deactivate-account.html"

    @method_decorator(login_required)
    def get(self, request):
        context = {'profile': request.user.profile}
        return self.return_success(request, context)

    def post(self, request):
        form = CoreDeactivateAccountForm(request, request.POST)

        if form.process():
            return redirect('/')

        context = {
            'profile': request.user.profile,
            'form': form
        }
        return self.return_success(request, context)


