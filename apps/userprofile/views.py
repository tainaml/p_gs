# coding=utf-8
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.core.urlresolvers import reverse
from django.db import models
from django.http import Http404, HttpResponse
from django.shortcuts import render, redirect
from django.utils.decorators import method_decorator
from django.utils.translation import ugettext as _
from django.views.generic import View
from django.views.decorators.http import require_POST

from apps.userprofile.models import GenderType
from apps.userprofile.service import business as Business
from apps.userprofile.service.forms import EditProfileForm, OccupationForm


class ProfileBaseView(View):

    not_found = Http404(_('Profile not Found.'))
    user_not_found = Http404(_('User not Found.'))

    def filter(self, request, user_or_username=None):

        if user_or_username and isinstance(user_or_username, unicode):
            user = Business.get_user(user_or_username)
        elif user_or_username and isinstance(user_or_username, models.Model):
            user = user_or_username
        else:
            user = None

        if not user:
            '''
            Only works when user exists
            '''
            raise self.user_not_found

        profile = Business.get_profile(user)

        if not profile:
            '''
            Only works when community exists
            '''
            raise self.not_found

        return profile

    def get_context(self, request, profile_instance=None):
        return {}


class ProfileShowView(ProfileBaseView):

    template_path = 'userprofile/profile.html'

    def get(self, request, username):

        profile = self.filter(request, username)

        context = {'profile': profile}
        context.update(self.get_context(request, profile))

        return render(request, self.template_path, context)


class ProfileEditView(ProfileBaseView):

    template_path = 'userprofile/edit_form.html'
    form_profile = EditProfileForm

    @method_decorator(login_required)
    def get(self, request, *args, **kwargs):

        profile = self.filter(request, request.user)

        countries = Business.get_countries()
        form = self.form_profile(data_model=profile)

        context = {
            'form': form,
            'countries': countries,
            'gender': GenderType(),
        }
        context.update(self.get_context(request, profile))

        return render(request, self.template_path, context)

    @method_decorator(login_required)
    def post(self, request, *args, **kwargs):

        profile = self.filter(request, request.user)
        if profile.city:
            states = Business.get_states(profile.city.state.country.id)
            cities = Business.get_cities(profile.city.state.id)
        else:
            states = None
            cities = None

        countries = Business.get_countries()
        form = self.form_profile(request.user, profile, request.POST, request.FILES)

        if form.process():
            messages.add_message(request, messages.SUCCESS, _("Profile edited successfully!"))
            return redirect(reverse('profile:edit'))

        context = {
            'form': form,
            'countries': countries,
            'states': states,
            'cities': cities,
            'gender': GenderType()
        }

        return render(request, self.template_path, context)


class ProfileGetState(ProfileBaseView):

    template_path = 'userprofile/components/select_options.html'

    def post(self, request, *args, **kwargs):
        states = Business.get_states(country_id=request.POST['country_id'])

        context = {
            'items': states,
            'message': _("Select a state")
        }

        return render(request, self.template_path, context)


class ProfileGetCity(ProfileBaseView):

    template_path = 'userprofile/components/select_options.html'

    def post(self, request, *args, **kwargs):
        cities = Business.get_cities(state_id=request.POST['state_id'])

        context = {
            'items': cities,
            'message': _("Select a city")
        }

        return render(request, self.template_path, context)


class OccupationManageView(ProfileBaseView):

    template_path = 'userprofile/occupation_manage.html'

    @method_decorator(login_required)
    def get(self, request):

        profile = self.filter(request, request.user)
        # occupations = Business.get_occupations({'profile': profile}, order_by='id')
        # occupations = profile.occupation_set.all().order_by('id')
        occupations = profile.occupation.order_by('id')

        context = {
            'profile': profile,
            'occupations': occupations
        }
        context.update(self.get_context(request, profile))

        return render(request, self.template_path, context)


class OccupationAddView(ProfileBaseView):

    template_path = 'userprofile/occupation_add.html'
    form_occupation = OccupationForm

    @method_decorator(login_required)
    def get(self, request):

        form = self.form_occupation()

        context = {'form': form}
        context.update(self.get_context(request))

        return render(request, self.template_path, context)

    @method_decorator(login_required)
    def post(self, request):

        form = self.form_occupation(request.POST, request)
        if form.process():
            messages.add_message(request, messages.SUCCESS, _("Occupation created successfully!"))
            return redirect(reverse('profile:occupation_manage'))

        context = {'form': form}
        context.update(self.get_context(request))

        return render(request, self.template_path, context)


class OccupationShowView(ProfileBaseView):

    template_path = 'userprofile/occupation_show.html'

    @method_decorator(login_required)
    def get(self, request, occupation_id):

        profile = self.filter(request, request.user)
        occupation = Business.get_occupation({'id': occupation_id})

        if not occupation:
            raise self.not_found

        context = {
            'profile': profile,
            'occupation': occupation
        }
        context.update(self.get_context(request, profile))

        return render(request, self.template_path, context)


class OccupationEditView(ProfileBaseView):

    template_path = 'userprofile/occupation_edit.html'
    form_occupation = OccupationForm

    @method_decorator(login_required)
    def get(self, request, occupation_id=None):

        occupation = Business.get_occupation({'id': occupation_id})

        if not occupation:
            raise self.not_found

        form = self.form_occupation(data_model=occupation)

        context = {
            'form': form,
            'occupation': occupation
        }
        context.update(self.get_context(request))

        return render(request, self.template_path, context)

    @method_decorator(login_required)
    def post(self, request, occupation_id=None):

        occupation = Business.get_occupation({'id': occupation_id})

        if not occupation:
            raise self.not_found

        form = self.form_occupation(request.POST, instance=occupation)
        if form.process():
            messages.add_message(request, messages.SUCCESS, _("Occupation updated successfully!"))
            return redirect(reverse('profile:occupation_manage'))

        context = {
            'form': form,
            'occupation': occupation
        }
        context.update(self.get_context(request))

        return render(request, self.template_path, context)


class OccupationDeleteView(ProfileBaseView):

    template_path = ''

    def return_error(self, request):
        messages.add_message(request, messages.ERROR, _("Error! Occupation was not deleted!"))
        return redirect(reverse('profile:occupation_manage'))

    def return_success(self, request):
        messages.add_message(request, messages.SUCCESS, _("Occupation deleted successfully!"))
        return redirect(reverse('profile:occupation_manage'))

    @method_decorator(login_required)
    def get(self, request, occupation_id=None, *args, **kwargs):

        if not occupation_id:
            raise self.not_found

        if Business.delete_occupation(occupation_id):
            return self.return_success(request)

        return self.return_error(request)


class ProfileFollowingsView(ProfileShowView):

    template_path = 'userprofile/profile-followings.html'


class ProfileFollowersView(ProfileShowView):

    template_path = 'userprofile/profile-followers.html'


class ProfileCommunitiesView(ProfileShowView):

    template_path = 'userprofile/profile-communities.html'