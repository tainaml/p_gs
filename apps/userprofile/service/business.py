from django.contrib.auth import authenticate
from django.contrib.auth.models import User
from django.utils.translation import ugettext as _
from django.db import transaction

from apps.userprofile.models import UserProfile, Country, State, City


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


def update_profile(user, data=None):
    profile = check_profile_exists(user)

    dt = data
    print dt
    print dt['occupation']

    if profile:
        profile.birth = data['birth']
        profile.gender = data['gender']
        profile.city = data['city']

    profile.save()
    return profile


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