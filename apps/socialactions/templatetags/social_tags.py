from distutils.command.register import register
from django.http import Http404
from django import template
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
def followers_box(context, content_object, url_next):
    try:
        followers = Business.get_users_acted_by_model(model=content_object,
                                                      action=settings.SOCIAL_FOLLOW,
                                                      itens_per_page=9,
                                                      page=1)

    except ValueError:
        raise Http404()

    return {
        'followers': followers,
        'content_type': followers[0].content_type if followers and followers[0].content_type else None,
        'object': content_object,
        'page': (followers.number if followers and followers.number else 0) + 1,
        'url_next': url_next,
        'request': context['request']
    }


@register.inclusion_tag('socialactions/followings_box.html', takes_context=True)
def followings_box(context, author, content_type, url_next):
    try:
        followings = Business.get_users_acted_by_author(author=author,
                                                        action=settings.SOCIAL_FOLLOW,
                                                        content_type=content_type,
                                                        items_per_page=9,
                                                        page=1)

    except ValueError:
        raise Http404()

    return {
        'followings': followings,
        'content_type': followings[0].content_type if followings and followings[0].content_type else None,
        'object': author,
        'page': (followings.number if followings and followings.number else 0) + 1,
        'url_next': url_next,
        'request': context['request']
    }


@register.inclusion_tag('socialactions/followers_partial_actions.html', takes_context=True)
def follow_action(context, object_to_link, url_next, btn_class="btn-sm perfil-button"):

    try:
        content = Business.get_content_by_object(object_to_link)

        followings = Business.get_users_acted_by_author(author=context['request'].user,
                                                        action=settings.SOCIAL_FOLLOW,
                                                        content_type=content.model)
        following_list = []
        for following in followings:
            following_list.append(following.content_object.id)

    except ValueError:
        raise Http404()

    return {
        'object_to_link': object_to_link.id,
        'content': content.model,
        'followings': following_list,
        'url_next': url_next,
        'request': context['request'],
        'btn_class': btn_class
    }


@register.simple_tag()
def followers_count(user):

    try:
        count = Business.followers_count(content_object=user)
    except ValueError:
        raise Http404()

    return count