from abc import ABCMeta, abstractmethod
from apps.core.forms.community import CoreCommunityFormSearch
from apps.core.forms.wizard import StepOneWizardForm
from apps.core.tasks import notify_by_email_user_friends
from apps.core.utils import build_absolute_uri
from apps.taxonomy.models import Taxonomy
from apps.userprofile.models import Responsibility
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from django.http.response import Http404
from django.shortcuts import redirect, render
from django.urls import reverse
from django.utils.decorators import method_decorator
from django.views import View
from apps.userprofile.service import business as BusinessUserProfile
from ..business import community as Business
from rede_gsti import settings
import copy


class CoreProfileWizard(View):

    __metaclass__ = ABCMeta
    form = None
    template_name = None
    user = None

    @method_decorator(login_required)
    def get(self, request, step):

        if request.user.user_profile.wizard_step >= step:
            return redirect(to='profile:feed')

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

        data = copy.copy(request.POST)
        data.update({
            'wizard_step': step
        })

        form = self.form(data=data, files=request.FILES, user=self.user)

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
        responsabilities = Responsibility.objects.filter(avaiable_to_choose=True).only("id", "name").order_by("name")

        context.update({
            'states': states,
            'cities': cities,
            'responsibilities': responsabilities
        })

        return context


class StepTwoWizard(CoreProfileWizard):

    template_name = 'core/partials/wizard/wizard-step-two.html'
    form = CoreCommunityFormSearch

    def get_context(self, request, step, context=None):

        context = super(StepTwoWizard, self).get_context(request, step, context)

        context.update({
            'categories': Taxonomy.objects.filter(term__description="Categoria")
        })

        return context

    def get(self, request, step):

        if request.user.user_profile.wizard_step >= step:
            return redirect(to='profile:feed')

        context = self.get_context(request, step)

        return render(request, self.template_name, context)

    def post(self, request, step):

        if request.user.user_profile.wizard_step >= step:
            return redirect(to='profile:feed')

        context = self.get_context(request, step)

        taxonomies = request.POST.getlist('taxonomies')

        if not taxonomies:
            return render(request, self.template_name, context)

        request.session['wizard_step2_taxonomies'] = taxonomies
        return redirect(to="profile:wizard", step=step+1)


class StepThreeWizard(CoreProfileWizard):

    template_name = 'core/partials/wizard/wizard-step-three.html'
    template_segment_path = 'core/partials/wizard/community-segment.html'

    def get_context(self, request, step, context=None):
        context = super(StepThreeWizard, self).get_context(request, step, context)

        page = request.GET.get('page', 1)

        taxonomies = request.session.get('wizard_step2_taxonomies', None)
        criteria = request.GET.get('criteria', '')

        communities = Business.get_communities(
            taxonomies,
            criteria,
            6,
            page
        )

        communities = Paginator(communities, per_page=6)

        try:
            pagination = communities.page(page)
        except PageNotAnInteger:
            page = 1
            pagination = communities.page(page)
        except EmptyPage:
            page = communities.num_pages
            pagination = communities.page(communities.num_pages)


        context.update({
            'communities': pagination,
            'taxonomies': taxonomies,
            'criteria': criteria,
            'page': (int(page) + 1) if pagination.has_next() else False,
        })
        return context

    def return_error(self, request, context=None):
        pass

    def return_success(self, request, context=None):
        if not context:
            context = {}
        _context = context
        return render(request, self.template_segment_path, _context, status=200)

    def get(self, request, step):

        if request.user.user_profile.wizard_step >= step:
            return redirect(to='profile:feed')

        context = self.get_context(request, step)

        if 'taxonomies' not in context:
            return redirect(to="profile:wizard", step=2)

        if request.is_ajax():
            return self.return_success(request, context)

        return render(request, self.template_name, context)

    def post(self, request, step):

        user_profile = request.user.user_profile
        user_profile.wizard_step = 3
        user_profile.save()

        del request.session['wizard_step2_taxonomies']

        notify_by_email_user_friends.delay(request.user.id)

        return redirect(to="profile:wizard-success")


class WizardSuccessView(View):

    template_name = 'core/partials/wizard/wizard-success.html'

    @method_decorator(login_required)
    def get(self, request):
        last_step = getattr(settings, 'WIZARD_STEPS_TOTAL')
        referer = request.META.get("HTTP_REFERER", None)
        last_step_url = build_absolute_uri(reverse("profile:wizard", args=[last_step]))

        if not getattr(settings, 'DEBUG', False) and last_step_url != referer:
            redirect(reverse('profile:feed'))

        return render(request, self.template_name)


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
