__author__ = 'phillip'
from django.contrib.contenttypes.models import ContentType
from django import template
from django.http import Http404
register = template.Library()

@register.inclusion_tag('comment/create.html', takes_context=True)
def box_comment(context, content_object, url_next):

    try:
        content_type = ContentType.objects.get_for_model(content_object)

        pass

    except ValueError:
        raise Http404()

    return {
        'content_object_id': content_object.id,
        'content_type': content_type,
        'url_next': url_next,
        'request': context['request']
    }