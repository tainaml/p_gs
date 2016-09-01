from django import template
from django.conf import settings
register = template.Library()

@register.inclusion_tag("core/templatetags/tag-manager.html")
def tag_manager():
    must_be_rendered = (settings.ENVIRONMENT == 'production')


    return {
        'must_be_rendered': must_be_rendered
    }