from distutils.command.register import register

from django import template
from django.http import Http404

from ..service import business as Business

register = template.Library()


@register.inclusion_tag('community/templatetags/community-box.html', takes_context=True)
def community_box(context, community):

    try:
        community = Business.get_community(community.slug)
    except ValueError:
        raise Http404()

    return {
        'community': community,
        'request': context['request']
    }