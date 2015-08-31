from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.core.urlresolvers import reverse
from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.views.decorators.http import require_POST
from django.utils.translation import ugettext as _

from apps.userprofile.service import business as Business
from apps.userprofile.models import Country, State, City, GenderType
from apps.userprofile.service.forms import EditProfileForm


def show(request, username):
    profile = Business.check_profile_exists(Business.get_user(username))
    profile.gender_text = GenderType.LABEL[profile.gender]

    return render(request, 'userprofile/show.html', {'profile': profile, 'gender': GenderType})


@login_required
def edit(request):

    countries = Business.get_countries()

    profile = Business.get_profile(request.user)

    form = EditProfileForm(data_model=profile)

    if profile.city:
        states = Business.get_states(profile.city.state.country.id)
        cities = Business.get_cities(profile.city.state.id)
    else:
        states = None
        cities = None

    return render(request, 'userprofile/edit_form.html', {
        'form': form,
        'countries': countries,
        'states': states,
        'cities': cities,
        'gender': GenderType(),
    })


@login_required
@require_POST
def update_profile(request):

    countries = Business.get_countries()

    profile = Business.get_profile(request.user)

    form = EditProfileForm(request.POST, request=request, set_queryset=request.POST['state'])

    if profile.city:
        states = Business.get_states(profile.city.state.country.id)
        cities = Business.get_cities(profile.city.state.id)
    else:
        states = None
        cities = None

    if form.process():
        messages.add_message(request, messages.SUCCESS, _("Profile edited successfully!"))
        return redirect(reverse('profile:edit'))

    return render(request, 'userprofile/edit_form.html', {
        'form': form,
        'countries': countries,
        'states': states,
        'cities': cities,
        'gender': GenderType(),
        })


@require_POST
def get_state(request):
    states = Business.get_states(country_id=request.POST['country_id'])
    return render(request, 'userprofile/components/select_options.html', {
        'items': states,
        'message': _("Select a state")
    })


@require_POST
def get_city(request):
    cities = Business.get_cities(state_id=request.POST['state_id'])
    return render(request, 'userprofile/components/select_options.html', {
        'items': cities,
        'message': _("Select a city")
    })