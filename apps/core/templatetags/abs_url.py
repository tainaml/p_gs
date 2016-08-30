from django import template
from django.core.urlresolvers import reverse
from ..utils import reverse_absolute

register = template.Library()

@register.simple_tag(takes_context=True)
def absolute_url(context, parser, *token):
    path = reverse(parser, args=token)
    request_obj = context['request']
    return reverse_absolute(request_obj, path)


@register.assignment_tag(takes_context=True)
def absolute_from_path(context, path):
    request_obj = context['request']
    return reverse_absolute(request_obj, path)