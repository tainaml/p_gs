from django.contrib.auth import authenticate
from django.contrib.auth.models import User
from django.utils.translation import ugettext as _
from django.db import transaction

from apps.userprofile.models import UserProfile, Country, State, City, Occupation


def check_user_exists(username_or_email=None):

    user = User.objects.get(username=username_or_email)
    if not user:
        try:
            user = User.objects.get(email=username_or_email)
        except User.DoesNotExist:
            user = False

    return user


def get_user(username_or_email=None):
    return check_user_exists(username_or_email) if username_or_email else None


def check_profile_exists(user=None):

    user = User.objects.get(id=user.id)

    try:
        profile = UserProfile.objects.get(user=user)
    except UserProfile.DoesNotExist:
        profile = create_profile(user)

    return profile


def get_profile(user=None):
    return check_profile_exists(user) if user else None


def create_profile(user, data=None):
    profile = UserProfile(user=user)
    profile.save()

    return profile


@transaction.atomic()
def edit_profile(user, data_profile=None, data_formset=None):

    try:
        if data_profile:
            profile = update_profile(user, data_profile)

        if data_formset:
            for data in data_formset:
                create_occupation(user, data)
    except:
        return False

    return profile


def update_profile(user=None, data=None):

    profile = check_profile_exists(user)

    try:
        profile.birth = data['birth']
        profile.gender = data['gender']
        profile.city = data['city']
        profile.save()
    except:
        return False

    return profile


def create_occupation(user=None, data=None):

    profile = get_profile(user)

    try:
        occupation = Occupation()
        occupation.responsibility = data['responsibility']
        occupation.description = data['description']
        occupation.profile = profile
        occupation.save()
    except:
        return False

    return occupation


def get_countries(country_id=None):
    if country_id:
        return Country.objects.get(id=country_id)

    return Country.objects.all()


def get_states(country_id=None):
    if country_id:
        return State.objects.filter(country=country_id)

    return State.objects.all()


def get_cities(state_id=None):
    if state_id:
        return City.objects.filter(state=state_id)

    return City.objects.all()


def get_occupations(user):

    try:
        profile = get_profile(user)
        occupations = Occupation.objects.filter(profile=profile.id)
    except:
        return False

    return occupations


def get_occupation(params={}):

    try:
        occupations = Occupation.objects.get(**params)
    except:
        return False

    return occupations