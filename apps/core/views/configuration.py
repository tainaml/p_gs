from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.shortcuts import render
from django.utils.decorators import method_decorator
from django.views.generic import View
from apps.core.forms.configuration import ConfigNotificationsForm


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

    form = ConfigNotificationsForm

    @method_decorator(login_required)
    def get(self, request):

        context = {'profile': request.user.profile}
        return self.return_success(request, context)

    @method_decorator(login_required)
    def post(self, request):

        form = self.form(request.POST)
        form.set_entity(request.user)

        if form.process():
            return JsonResponse({}, status=200)

        return JsonResponse({}, status=400)