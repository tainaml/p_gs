from django.http import Http404
from django import template
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