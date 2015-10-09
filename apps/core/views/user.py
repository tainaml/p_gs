from django.http import JsonResponse
from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator

from apps.core.business import community as BusinessCoreCommunity
from apps.core.forms.community import CoreCommunityFormSearch
from apps.core.forms.user import CoreUserSearchForm, CoreUserProfileEditForm
from apps.userprofile import views
from apps.userprofile.service import business as BusinessUserprofile
from apps.taxonomy.service import business as BusinessTaxonomy


class CoreUserSearchView(views.ProfileShowView):

    template_path = 'userprofile/profile.html'

    def get_context(self, request, profile_instance=None):
        context = super(CoreUserSearchView, self).get_context(request, profile_instance)
        itens_by_page = 10

        self.form = CoreUserSearchForm(
            profile_instance,
            ['article', 'question'],
            itens_by_page,
            request.user,
            request.GET
        )

        feed_objects = self.form.process()

        context.update({'feed_objects': feed_objects, 'form': self.form, 'page': self.form.cleaned_data.get('page', 0) + 1})

        return context

    def get(self, request, **kwargs):

        profile = self.filter(request, request.user)

        context = {'profile': profile}
        context.update(self.get_context(request, profile))

        return render(request, self.template_path, context)


class CoreUserList(CoreUserSearchView):
    template_path = 'userprofile/partials/profile-list.html'

    def get_context(self, request, profile_instance=None):
        context = super(CoreUserSearchView, self).get_context(request, profile_instance)

        return context


class CoreUserFeed(CoreUserSearchView):
    template_path = 'userprofile/profile.html'

    @method_decorator(login_required)
    def get(self, request, **kwargs):
        return super(CoreUserFeed, self).get(request)

    def get_context(self, request, profile_instance=None):
        context = super(CoreUserFeed, self).get_context(request, profile_instance)

        states = BusinessUserprofile.get_states(1)
        cities = BusinessUserprofile.get_cities(profile_instance.city.state.id) if profile_instance.city else None
        responsibilities = BusinessUserprofile.get_responsibilities()
        categories = BusinessTaxonomy.get_categories()

        context.update({
            'states': states,
            'cities': cities,
            'categories': categories,
            'responsibilities': responsibilities
        })
        return context


class CoreProfileEditAjax(views.ProfileEditView):

    form_profile = CoreUserProfileEditForm

    def return_error(self, request, context=None):
        _response_context = {}

        if 'form' in context:
            _form = context['form']
            _response_context = {'errors': _form.errors}

        return JsonResponse(_response_context, status=400)

    def return_success(self, request, context=None):
        return JsonResponse(context, status=200)


class CoreProfileWizardStepOneAjax(CoreProfileEditAjax):

    def get_context(self, request, profile_instance=None):
        profile = BusinessUserprofile.update_wizard_step(profile_instance, 1)
        return {'step': profile.wizard_step}


class CoreProfileWizardStepTwoAjax(views.ProfileBaseView):

    template_segment_path = 'core/partials/wizard/community-segment.html'

    def return_error(self, request, context=None):
        if not context:
            context = {}

        _context = context

        return JsonResponse(_context, status=400)

    def return_success(self, request, context=None):
        if not context:
            context = {}

        _context = {}
        _context['page'] = context['page']
        _context['taxonomies'] = context['taxonomies']

        _context['template'] = render(request, self.template_segment_path, {
            'communities': context['communities'],
            'taxonomies': context['taxonomies'],
            'page': context['page']
        }).content

        return JsonResponse(_context, status=200)

    def get_context(self, request, profile_instance=None):
        profile = BusinessUserprofile.update_wizard_step(profile_instance, 2)
        return {'step': profile.wizard_step}

    @method_decorator(login_required)
    def get(self, request, *args, **kwargs):

        profile = self.filter(request, request.user)

        context = {}

        if 'taxonomies' not in request.GET:
            context.update({'status': 400})
            return self.return_error(request, context)

        form = CoreCommunityFormSearch(3, request.GET)
        communities = form.process()
        taxonomies = [taxonomy.id for taxonomy in form.cleaned_data['taxonomies']]

        context['status'] = 200
        context['taxonomies'] = taxonomies
        context['communities'] = communities
        context['page'] = form.cleaned_data['page'] + 1

        context.update(self.get_context(request, profile))
        return self.return_success(request, context)


    @method_decorator(login_required)
    def post(self, request, *args, **kwargs):

        profile = self.filter(request, request.user)

        context = {}
        context.update(self.get_context(request, profile))

        if 'taxonomies' in request.POST:
            taxonomy_categories_obj = BusinessTaxonomy.get_categories(request.POST.getlist('taxonomies'))
            taxonomy_communities = BusinessTaxonomy.get_related_list_top_down(taxonomy_categories_obj)
            taxonomies = [tax.id for tax in taxonomy_communities]

            form = CoreCommunityFormSearch(3, {"taxonomies": taxonomies})
            communities = form.process()

            context['status'] = 200
            context['taxonomies'] = taxonomies
            context['communities'] = communities
            context['page'] = communities.number + 1

            context['template'] = render(request, self.template_segment_path, {
                'communities': communities,
                'taxonomies': taxonomies,
                'page': communities.number + 1
            }).content

            return self.return_success(request, context)

        return self.return_error(request, context)


class CoreProfileWizardStepTwoListAjax(CoreProfileWizardStepTwoAjax):

    def return_error(self, request, context=None):
        pass

    def return_success(self, request, context=None):
        if not context:
            context = {}

        _context = context

        return render(request, self.template_segment_path, _context, status=200)

    def get_context(self, request, profile_instance=None):
        return {}


class CoreProfileWizardStepThreeAjax(views.ProfileBaseView):
    pass
