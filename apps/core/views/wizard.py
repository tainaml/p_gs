from abc import ABCMeta, abstractmethod
from apps.core.forms.user import CoreUserProfileEditStepOne
from apps.core.forms.wizard import StepOneWizardForm
from apps.userprofile.models import Responsibility
from django.contrib.auth.decorators import login_required
from django.http.response import Http404
from django.shortcuts import redirect, render
from django.utils.decorators import method_decorator
from django.views import View
from apps.userprofile.service import business as BusinessUserProfile


class CoreProfileWizard(View):

    __metaclass__ = ABCMeta
    form = None
    template_name = None
    user = None

    @method_decorator(login_required)
    def get(self, request, step):

        self.user = request.user

        form = self.form(user=self.user)

        context = self.get_context(request, step)
        context.update({
            'form': form
        })
        return render(request, self.template_name, context)

    @method_decorator(login_required)
    def post(self, request, step):

        self.user = request.user

        form = self.form(data=request.POST, files=request.FILES, user=self.user)

        if form.process():
            next_step = step + 1
            return redirect(to="profile:wizard", step=next_step)

        context = self.get_context(request, step)
        context.update({
            'form': form
        })
        return render(request, self.template_name, context)


    @abstractmethod
    def get_context(self, request, step, context=None):
        context = context if context else {}
        context.update({
            'step': step
        })
        return context


class StepOneWizard(CoreProfileWizard):

    template_name = 'core/partials/wizard/wizard-step-one.html'
    form = StepOneWizardForm

    def get_context(self, request, step, context=None):

        user_profile = request.user.user_profile
        context = super(StepOneWizard, self).get_context(request, step, context)
        states = BusinessUserProfile.get_states(1)
        cities = BusinessUserProfile.get_cities(user_profile.city.state.id) if user_profile.city else None
        responsabilities = Responsibility.objects.all().only("id", "name").order_by("name")

        context.update({
            'states': states,
            'cities': cities,
            'responsibilities': responsabilities
        })

        return context


class StepTwoWizard(CoreProfileWizard):
    pass


class StepThreeWizard(CoreProfileWizard):
    pass


@login_required
def wizard_proxy_view(request, step):

    MAPPER_VIEWS = {
        1: StepOneWizard,
        2: StepTwoWizard,
        3: StepThreeWizard,
    }

    step = int(step)

    if not step or step == 0:
        return redirect(to="profile:wizard", step=1)

    if step in MAPPER_VIEWS.keys():
        view_class = MAPPER_VIEWS.get(step)
        return view_class.as_view()(request, step)
    else:
        raise Http404('Step not found')
