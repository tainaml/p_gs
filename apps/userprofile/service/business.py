from django.contrib.auth import authenticate
from django.contrib.auth.models import User
from django.utils.translation import ugettext as _
from django.db import transaction
from apps.taxonomy.models import Term, Taxonomy

from apps.userprofile.models import UserProfile, Country, State, City, Occupation, Responsibility


def check_user_exists(username_or_email=None):

    try:
        user = User.objects.get(username=username_or_email)
        if not user:
            user = User.objects.get(email=username_or_email)
    except User.DoesNotExist:
        user = False

    return user


def get_user(username_or_email=None):
    return check_user_exists(username_or_email) if username_or_email else None


def check_profile_exists(user=None):

    user = get_user(user.username)

    try:
        profile = UserProfile.objects.get(user=user)
    except User.DoesNotExist:
        profile = False
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
        profile = update_profile(user, data_profile)

        if data_formset:
            for data in data_formset:
                create_occupation(user, data)
    except:
        return False

    return profile


def update_profile(user=None, data=None):

    profile = get_profile(user)

    if data:
        try:
            profile.birth = data['birth']
            profile.gender = data['gender']
            profile.city = data['city']

            if data.get('city_hometown'):
                profile.city_hometown = data.get('city_hometown')

            if data['profile_picture'] and profile.profile_picture != data['profile_picture']:
                profile.profile_picture.delete()
                profile.profile_picture = data['profile_picture']

            profile.save()
        except:
            return False

    return profile

def update_user(user, data={}):

    try:
        user = User.objects.filter(id=user.id).update(**data)
    except:
        return False

    return user


def update_wizard_step(profile, step=0):

    try:
        profile.wizard_step = step
        profile.save()
    except:
        return None

    return profile


def create_occupation(profile=None, user=None, data=None):

    if not data:
        data = {}

    if profile:
        profile = profile
    elif user:
        profile = get_profile(user)

    data.update({'profile': profile})

    try:
        occupation = Occupation(**data)
        occupation.save()
    except:
        return False

    return occupation


def update_or_create_occupation(profile=None, user=None, data=None):

    if not data:
        data = {}

    if profile:
        profile = profile
    elif user:
        profile = get_profile(user)

    data.update({'profile': profile})

    try:
        occupation = Occupation.objects.update_or_create(**data)
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


def get_occupations(params={}, order_by=None):

    try:
        occupations = Occupation.objects.filter(**params).order_by(order_by)
    except:
        return False

    return occupations


def get_occupation(params={}):

    try:
        occupations = Occupation.objects.get(**params)
    except:
        return False

    return occupations


def delete_occupation(occupation_id):

    try:
        occupation = get_occupation({'id': occupation_id})
        occupation.delete()
    except:
        return False
    return True


def update_occupation(occupation, data):
    try:
        occupation.responsibility = data['responsibility']
        occupation.description = data['company']
        occupation.save()
    except:
        return False

    return occupation


def get_responsibilities():

    try:
        responsibilities = Responsibility.objects.all()
    except Responsibility.DoesNotExist:
        return False

    return responsibilities


def get_categories():
    term = Term.objects.filter(description="Categoria")
    categories = Taxonomy.objects.filter(term=term)

    return categories
