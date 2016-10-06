from django import template
from django.conf import settings
register = template.Library()

@register.inclusion_tag("core/templatetags/tag-manager-script.html")
def tag_manager_script():
    must_be_rendered = (settings.ENVIRONMENT == 'production')


    return {
        'must_be_rendered': must_be_rendered
    }

@register.inclusion_tag("core/templatetags/tag-manager-iframe.html")
def tag_manager_iframe():
    must_be_rendered = (settings.ENVIRONMENT == 'production')


    return {
        'must_be_rendered': must_be_rendered
    }