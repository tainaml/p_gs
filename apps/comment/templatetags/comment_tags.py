from django.conf import settings

__author__ = 'phillip'
from django.contrib.contenttypes.models import ContentType
from ..models import Comment
from django import template
from django.http import Http404
register = template.Library()


@register.inclusion_tag('comment/create.html', takes_context=True)
def box_comment(context, content_object, url_next, **kwargs):

    try:
        content_type = ContentType.objects.get_for_model(content_object)
    except ValueError, e:
        raise Http404()

    return_dict = {
        'content_object': content_object,
        'content_type': content_type.model,
        'url_next': url_next,
        'request': context['request'],


    }
    return_dict.update(kwargs)

    return return_dict



@register.inclusion_tag('comment/edit.html')
def box_edit_comment(instance, url_next):

    return {
        'instance': instance,
        'url_next': url_next
    }


@register.inclusion_tag('comment/list-comment.html', takes_context=True)
def list_comment(context, content_object, **kwargs):

    try:
        content = ContentType.objects.get_for_model(content_object)

        list_comment = Comment.objects.filter(content_type=content, object_id=content_object.id).order_by('-creation_date')
        max_levels = settings.MAX_LEVELS if hasattr(settings, 'MAX_LEVELS') else False

    except ValueError:
        raise Http404()

    return_dict = {
        'list_comment': list_comment,
        'request': context['request'],
        'max_levels': max_levels
    }
    return_dict.update(kwargs)

    return return_dict
