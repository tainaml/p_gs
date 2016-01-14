from distutils.command.register import register

from django import template
from django.http import Http404

from ..service import business as Business

register = template.Library()


@register.assignment_tag
@register.simple_tag()
def articles_count(author):

    try:
        count = Business.count_articles(author=author)
    except ValueError:
        raise Http404()

    return count