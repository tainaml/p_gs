from django import template
from django.conf import settings
register = template.Library()

@register.inclusion_tag('core/templatetags/ads.html', takes_context=True)
def ads_only_production(context, location, device):
    must_be_rendered = True
    request= context['request']

    if settings.ENVIRONMENT == "production":
        if device.lower() != "all":
            if (request.user_agent.is_mobile or request.user_agent.is_tablet) and device=="pc":
                must_be_rendered = False
            elif request.user_agent.is_pc and device=="touchable":
                must_be_rendered = False
    else:
        must_be_rendered = False

    return {
        'must_be_rendered': must_be_rendered,
        'location': location
    }