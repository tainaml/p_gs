from distutils.command.register import register
from django import template

from apps.userprofile.models import GenderType
from apps.userprofile.service import business as BusinessUserprofile
from apps.taxonomy.service import business as BusinessTaxonomy
from django.conf import settings

register = template.Library()


@register.inclusion_tag('core/templatetags/wizard.html', takes_context=True)
def wizard(context):

    request = context.get('request')

    if not request.user.is_authenticated():
        return

    profile = request.user.profile

    if profile.wizard_step < getattr(settings, 'WIZARD_STEPS_TOTAL'):

        BRAZIL_ID = 1

        states = BusinessUserprofile.get_states(BRAZIL_ID)
        cities = BusinessUserprofile.get_cities(profile.city.state.id) if profile and profile.city else None

        responsibilities = BusinessUserprofile.get_responsibilities()
        categories = BusinessTaxonomy.get_categories()

        response_data = {
            'request': request,
            'wizard_profile': profile,
            'gender': GenderType(),
            'states': states,
            'cities': cities,
            'responsibilities': responsibilities,
            'categories': categories
        }
    else:
        response_data = {}

    return response_data
