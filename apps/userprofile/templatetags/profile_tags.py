from distutils.command.register import register
from django import template
from django.http import Http404
from rede_gsti import settings
from ..service import business as Business


register = template.Library()


@register.inclusion_tag('userprofile/templatetags/profile-box.html', takes_context=True)
def profile_box(context, user):

    try:
        profile = Business.get_profile(user)
    except ValueError:
        raise Http404()

    return {
        'profile': profile,
        'request': context['request']
    }