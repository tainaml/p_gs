__author__ = 'phillip'

from django.contrib.contenttypes.models import ContentType
from django import template
from django.http import Http404

from apps.comment.service import business as CommentBusiness

register = template.Library()


@register.inclusion_tag('comment/comment-module.html')
def module_comment(content_object, **kwargs):

    try:
        comments = CommentBusiness.get_comments_by_content_object(content_object)

    except ValueError, e:
        raise Http404()


    return_dict = {
        'content_object': content_object,
        'content_type': ContentType.objects.get_for_model(content_object),
        'comments': comments
    }

    return_dict.update(kwargs)

    return return_dict

