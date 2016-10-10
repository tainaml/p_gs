import logging

from apps.account.models import User
from django.db import transaction
from apps.account.models import User

from apps.taxonomy.models import Term, Taxonomy
from apps.userprofile.models import UserProfile, Occupation, Responsibility
from apps.geography.models import Country, State, City
from django.db.models import Q
from rede_gsti import settings

logger = logging.getLogger('general')


def check_user_exists(username_or_email=None):

    try:

        user = User.objects.prefetch_related(
            'profile'
        ).get(Q(username=username_or_email) | Q(email=username_or_email))

    except User.DoesNotExist:
        user = False

    return user


def get_user(username_or_email=None):
    return check_user_exists(username_or_email) if username_or_email else None


def check_profile_exists(user=None):

    try:

        profile = user.profile
        if isinstance(profile, UserProfile):
            return profile
        else:
            return profile.first()

    except Exception:
        pass

    # user = get_user(user.username)

    try:
        profile = UserProfile.objects.get(user=user)
    except User.DoesNotExist:
        profile = False
    except UserProfile.DoesNotExist:
        profile = create_profile(user)

    return profile


def get_profile(user=None):
    return user.profile
    # return check_profile_exists(user) if user else None


def create_profile(user, data=None):
    profile = UserProfile(user=user)
    profile.save()

    return profile


@transaction.atomic()
def edit_profile(user, data_profile=None):

    try:
        if user.email != data_profile['email']:
            user.email = data_profile['email']

        if user.first_name != data_profile['first_name']:
            user.first_name = data_profile['first_name']

        if user.last_name != data_profile['last_name']:
            user.last_name = data_profile['last_name']

        user.save()
        update_profile(user, data_profile)
    except Exception as e:
        if settings.DEBUG:
            logger.error(e.message)
        return False

    return user.profile


def update_profile(user=None, data=None):

    profile = user.profile if user and hasattr(user, 'profile') else get_profile(user)

    try:
        if data.get('birth'):
            profile.birth = data.get('birth')

        if data.get('gender'):
            profile.gender = data.get('gender')

        if data.get('city'):
            profile.city = data.get('city')

        if data.get('city_hometown'):
            profile.city_hometown = data.get('city_hometown')

        if data.get('profile_picture') and profile.profile_picture != data.get('profile_picture'):
            profile.profile_picture.delete()
            profile.profile_picture = data.get('profile_picture')

        _wizard_step = data.get('wizard_step', False)
        if _wizard_step and _wizard_step <= settings.WIZARD_STEPS_TOTAL:
            profile.wizard_step = _wizard_step

        profile.save()
    except Exception as e:
        if settings.DEBUG:
            logger.error(e.message)
        return False

    return profile


def update_user(user, data={}):

    try:
        user = User.objects.filter(id=user.id).update(**data)
    except Exception, e:
        if settings.DEBUG:
            logger.error(e.message)
        return False

    return user


def update_wizard_step(profile, step=0):

    try:
        profile.wizard_step = step
        profile.save()
    except Exception, e:
        if settings.DEBUG:
            logger.error(e.message)
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
    except Exception as e:
        if settings.DEBUG:
            logger.error(e.message)
        return False

    return occupation


@transaction.atomic()
def update_or_create_occupation(profile=None, user=None, responsibilities=None):

    if not responsibilities:
        raise ValueError

    if profile:
        profile = profile
    elif user:
        profile = get_profile(user)

    try:
        occupations = Occupation.objects.filter(profile=profile)

        responsibilities_already = [occupation.responsibility for occupation in occupations]
        responsibilities_to_delete = list(set(responsibilities_already) - set(responsibilities))

        for responsibility in responsibilities:
            if responsibility in responsibilities_already:
                continue

            occupation = Occupation(
                responsibility=responsibility,
                profile=profile
            )
            occupation.save()

        for responsibility in responsibilities_to_delete:
            if responsibility not in responsibilities:
                occupations.filter(responsibility=responsibility).delete()

    except Exception as e:
        if getattr(settings, 'DEBUG'):
            logger.error(e.message)
        return False

    return True


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
    else:
        return []


def get_occupations(params={}, order_by=None):

    try:
        occupations = Occupation.objects.filter(**params).order_by(order_by)
    except Exception, e:
        if settings.DEBUG:
            logger.error(e.message)
        return False

    return occupations


def get_occupation(params={}):

    try:
        occupations = Occupation.objects.get(**params)
    except Exception, e:
        if settings.DEBUG:
            logger.error(e.message)
        return False

    return occupations


def delete_occupation(occupation_id):

    try:
        occupation = get_occupation({'id': occupation_id})
        occupation.delete()
    except Exception, e:
        if settings.DEBUG:
            logger.error(e.message)
        return False
    return True


def update_occupation(occupation, data):
    try:
        occupation.responsibility = data['responsibility']
        occupation.description = data['company']
        occupation.save()
    except Exception as e:
        if settings.DEBUG:
            logger.error(e.message)
        return False

    return occupation


def get_responsibilities():

    try:
        responsibilities = Responsibility.objects.all().order_by('name')
    except Responsibility.DoesNotExist:
        return False

    return responsibilities


def get_categories():
    term = Term.objects.filter(description="Categoria")
    categories = Taxonomy.objects.filter(term=term)

    return categories
