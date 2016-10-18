from django import template
from django.core.urlresolvers import reverse
from ..utils import reverse_absolute

register = template.Library()

@register.assignment_tag(takes_context=True)
def absolute_url(context, parser, *token):

    request_obj = context['request']

    if not token or parser[1] == '/':
        path = parser
    else:
        path = reverse(parser, args=token)

    return reverse_absolute(request_obj, path)


@register.assignment_tag(takes_context=True)
def absolute_from_path(context, path):
    request_obj = context['request']
    return reverse_absolute(request_obj, path)