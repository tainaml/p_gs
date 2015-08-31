from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.core.urlresolvers import reverse
from django.forms import formset_factory, model_to_dict
from django.shortcuts import render, redirect
from django.views.decorators.http import require_POST
from django.utils.translation import ugettext as _

from apps.userprofile.service import business as Business
from apps.userprofile.models import GenderType
from apps.userprofile.service.forms import EditProfileForm, OccupationForm


def show(request, username):
    profile = Business.get_profile(Business.get_user(username))
    profile.gender_text = GenderType.LABEL[profile.gender]

    return render(request, 'userprofile/show.html', {'profile': profile, 'gender': GenderType})


@login_required
def edit(request):

    countries = Business.get_countries()

    profile = Business.get_profile(request.user)
    occupations = Business.get_occupations(request.user)

    initials = []
    for occupation in occupations:
        initials.append(model_to_dict(occupation))

    print initials

    form = EditProfileForm(data_model=profile)

    # OccupationFormSet = formset_factory(OccupationForm)
    # occupation_formset = OccupationFormSet(prefix='occupation', initial=initials)

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
        # 'formset': occupation_formset
    })


@login_required
@require_POST
def update_profile(request):

    countries = Business.get_countries()

    profile = Business.get_profile(request.user)

    # OccupationFormSet = formset_factory(OccupationForm, extra=0)
    # occupation_formset = OccupationFormSet(request.POST, prefix='occupation')
    form = EditProfileForm(request.POST, request=request)

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
        # 'formset': occupation_formset
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


def occupation_manage(request):
    profile = Business.get_profile(request.user)
    occupations = Business.get_occupations(request.user)

    return render(request, 'userprofile/occupation_manage.html', {'profile': profile, 'occupations': occupations})


def occupation_add(request):
    form = OccupationForm()
    return render(request, 'userprofile/occupation_add.html', {'form': form})


def occupation_create(request):
    form = OccupationForm(request, request.POST)
    if form.process():
        return redirect(reverse('profile:occupation_manage'))
    return render(request, 'userprofile/occupation_add.html', {'form': form})


def occupation_show(request, occupation_id):
    profile = Business.get_profile(request.user)
    occupation = Business.get_occupation({'id': occupation_id})

    return render(request, 'userprofile/occupation_show.html', {'profile': profile, 'occupation': occupation})


def occupation_edit(request, occupation_id):
    occupation = Business.get_occupation({'id': occupation_id})
    if occupation:
        form = OccupationForm(data_model=occupation)
        return render(request, 'userprofile/occupation_edit.html', {'form': form})
    else:
        return redirect(reverse('profile:occupation_manage'))


def occupation_delete(request, occupation_id):
    if occupation_id:
        if Business.delete_occupation(occupation_id):
            messages.add_message(request, messages.SUCCESS, _("Occupation deleted successfully!"))
            return redirect(reverse('profile:occupation_manage'))
        else:
            messages.add_message(request, messages.ERROR, _("Error"))
    else:
        messages.add_message(request, messages.ERROR, _("Occupation invalid"))

    return redirect(reverse('profile:occupation_manage'))