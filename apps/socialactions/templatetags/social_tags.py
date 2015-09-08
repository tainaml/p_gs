from distutils.command.register import register
from django.contrib.contenttypes.models import ContentType
from django.http import Http404
from django import template
from apps.socialactions.service.business import get_users_acted_by_model
from rede_gsti import settings
from ..service import business as Business

register = template.Library()


@register.inclusion_tag('socialactions/like_box.html', takes_context=True)
def like_box(context, object_to_link, url_next):
    try:
        content = Business.get_content_by_object(object_to_link)

        likes = Business.user_likes_by_object(user=context['request'].user,
                                              content_object=object_to_link)

        unlikes = Business.user_unlikes_by_object(user=context['request'].user,
                                                  content_object=object_to_link)

        i_liked = Business.user_liked_by_object(user=context['request'].user,
                                                content_object=object_to_link)

        i_unliked = Business.user_unliked_by_object(user=context['request'].user,
                                                    content_object=object_to_link)

    except ValueError:
        raise Http404()

    return {
        'object_to_link': object_to_link.id,
        'content': content,
        'likes': likes,
        'unlikes': unlikes,
        'i_liked': i_liked,
        'i_unliked': i_unliked,
        'url_next': url_next,
        'request': context['request']
    }


@register.inclusion_tag('socialactions/followers_box.html', takes_context=True)
def followers_box(context, content_object):

    try:
        followers = get_users_acted_by_model(model=content_object,
                                             action=settings.SOCIAL_FOLLOW,
                                             itens_per_page=10,
                                             page=1)
    except ValueError:
        raise Http404()

    return {
        'followers': followers,
        'content_type': followers[0].content_type if followers and followers[0].content_type else None,
        'object': content_object,
        'page': (followers.number if followers and followers.number else 0) + 1
    }