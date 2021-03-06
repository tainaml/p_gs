from django.http import Http404
from django import template
from apps.core.business.content_types import ContentTypeCached

from rede_gsti import settings
from ..service import business as Business

register = template.Library()


article_content_type = ContentTypeCached.objects.get(model='article').model
question_content_type = ContentTypeCached.objects.get(model='question').model
profile_status_content_type = ContentTypeCached.objects.get(model='profilestatus').model

@register.inclusion_tag('socialactions/like_box.html', takes_context=True)
def like_box(context, object_to_link, url_next, like_type=None):
    try:
        content = Business.get_content_by_object(object_to_link).model

        user = context['request'].user


        i_liked = Business.user_liked_by_object(user=user,content_object=object_to_link)
        i_unliked = Business.user_unliked_by_object(user=user, content_object=object_to_link)

        if content in [article_content_type, question_content_type, profile_status_content_type]:
            likes = object_to_link.like_count or Business.user_likes_by_object(user=user, content_object=object_to_link)
            unlikes =object_to_link.dislike_count or Business.user_unlikes_by_object(user=user, content_object=object_to_link)
        else:
            likes = Business.user_likes_by_object(user=user, content_object=object_to_link)
            unlikes =Business.user_unlikes_by_object(user=user, content_object=object_to_link)


    except ValueError:
        raise Http404()

    if like_type == "inline":
        like_box_template = "socialactions/like-box-inline.html"
    elif like_type == "share-box":
        like_box_template = "socialactions/like-box-share-box.html"
    elif like_type == "reply":
        like_box_template = "socialactions/like-box-reply.html"
    else:
        like_box_template = "socialactions/like-box-default.html"

    return {
        'object_to_link': object_to_link.id,
        'content': content,
        'likes': likes,
        'unlikes': unlikes,
        'i_liked': i_liked,
        'i_unliked': i_unliked,
        'url_next': url_next,
        'request': context['request'],
        'like_box_template': like_box_template
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
        'items': followings,
        'content_type': followings[0].content_type if followings and followings[0].content_type else None,
        'object': author,
        'page': (followings.number if followings and followings.number else 0) + 1,
        'url_next': url_next,
        'request': context['request']
    }


@register.inclusion_tag('socialactions/followers_partial_actions.html', takes_context=True)
def follow_action(context, object_to_link, url_next, btn_class="btn-sm perfil-button", ajax=False):

    try:
        content = Business.get_content_by_object(object_to_link)
        followed = Business.user_acted_by_object(user=context['request'].user,
                                                 content_object=object_to_link,
                                                 action_type='follow')

    except ValueError:
        raise Http404()

    return {
        'object_to_link': object_to_link,
        'content': content.model,
        'followed': followed,
        'url_next': url_next,
        'request': context['request'],
        'btn_class': btn_class,
        'ajax': ajax
    }


@register.assignment_tag
@register.simple_tag()
def followers_count(object_to_link):

    try:
        count = Business.followers_count(content_object=object_to_link)
    except ValueError:
        raise Http404()

    return count


@register.simple_tag()
def followings_count(author, content_type):

    try:
        count = Business.followings_count(author, content_type)
    except ValueError:
        raise Http404()

    return count


@register.inclusion_tag('socialactions/communities_box.html', takes_context=True)
def communities_box(context, user, url_next):
    try:
        communities = Business.get_users_acted_by_author(author=user,
                                                         action=settings.SOCIAL_FOLLOW,
                                                         content_type='community',
                                                         items_per_page=9,
                                                         page=1)

    except ValueError:
        raise Http404()

    return {
        'items': communities,
        'content_type': communities[0].content_type if communities and communities[0].content_type else None,
        'object': user,
        'page': (communities.number if communities and communities.number else 0) + 1,
        'url_next': url_next,
        'request': context['request']
    }