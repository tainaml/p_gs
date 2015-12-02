from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from django.utils.decorators import method_decorator
from django.views.generic import View


class CoreSettingsBaseView(View):
    pass


class CoreSettingsAccountView(CoreSettingsBaseView):

    template_path = "configuration/configuration-account.html"

    @method_decorator(login_required)
    def get(self, request):

        context = {
            'profile': request.user.profile
        }

        return render(request, self.template_path, context)