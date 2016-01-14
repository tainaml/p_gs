from distutils.command.register import register

from django import template
from django.http import Http404

from ..service import business as Business

register = template.Library()


@register.inclusion_tag('userprofile/templatetags/profile-box.html', takes_context=True)
def profile_box(context, user, axis="vertical"):

    try:
        profile = Business.get_profile(user)
    except ValueError:
        raise Http404()

    if axis == "horizontal":
        partial_template = "userprofile/templatetags/profile-box-horizontal.html"
    else:
        partial_template = "userprofile/templatetags/profile-box-vertical.html"

    return {
        'profile': profile,
        'request': context['request'],
        'partial_template': partial_template
    }