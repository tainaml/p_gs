from django import template
from django.conf import settings
register = template.Library()

@register.inclusion_tag("core/templatetags/tag-manager-script.html")
def tag_manager_script():
    must_be_rendered = (settings.ENVIRONMENT == 'production')


    return {
        'must_be_rendered': must_be_rendered
    }

@register.inclusion_tag("core/templatetags/amp-tag-manager-script.html")
def amp_tag_manager_script():
    must_be_rendered = (settings.ENVIRONMENT == 'production')


    return {
        'must_be_rendered': must_be_rendered
    }

@register.inclusion_tag("core/templatetags/amp-tag-manager-iframe.html")
def amp_tag_manager_iframe():
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


@register.simple_tag(takes_context=True)
def seo_feed_robots(context, noindex, nofollow):

    robots = []

    if noindex:
        robots.append('noindex')

    if nofollow:
        robots.append('nofollow')

    return ','.join(robots)
