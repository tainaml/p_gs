import json
from django.core import serializers
from django.http import JsonResponse
from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.views.generic import View

from apps.core.forms.user import CoreUserSearchForm
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
            request.GET
        )

        feed_objects = self.form.process()

        context.update({'feed_objects': feed_objects, 'form': self.form, 'page': self.form.cleaned_data['page'] + 1})

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

        categories = BusinessTaxonomy.get_categories()

        context.update({
            'states': states,
            'categories': categories
        })
        return context


class CoreProfileEditAjax(views.ProfileEditView):

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


class CoreProfileWizardStepTwoAjax(View):

    def return_error(self, request, context=None):
        if not context:
            context = {}

        _context = context

        return JsonResponse(_context, status=400)

    def return_success(self, request, context=None):
        if not context:
            context = {}

        _context = context

        return JsonResponse(_context, status=200)

    def get_context(self, request, profile_instance=None):
        return {}

    @method_decorator(login_required)
    def post(self, request, *args, **kwargs):
        context = {}
        context.update(self.get_context(request))

        return self.return_success(request, context)
