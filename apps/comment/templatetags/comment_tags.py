__author__ = 'phillip'
from django.contrib.contenttypes.models import ContentType
from ..models import Comment
from django import template
from django.http import Http404
register = template.Library()

@register.inclusion_tag('comment/create.html', takes_context=True)
def box_comment(context, content_object, url_next):

    try:
        content_type = ContentType.objects.get_for_model(content_object)

    except ValueError:
        raise Http404()

    return {
        'content_object': content_object,
        'content_type': content_type,
        'url_next': url_next,
        'request': context['request']
    }

@register.inclusion_tag('comment/list.html', takes_context=True)
def list_comment(context, content_object):

    try:
        content = ContentType.objects.get_for_model(content_object)
        list_comment = Comment.objects.filter(content_type=content, object_id=content_object.id).order_by('-creation_date')


    except ValueError:
        raise Http404()

    return {
        'list_comment': list_comment,
        'request': context['request']
    }