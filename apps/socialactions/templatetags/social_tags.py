from django.contrib.contenttypes.models import ContentType
from django.http import Http404
from ..models import ActionType, UserAction
from django import template

register = template.Library()

@register.inclusion_tag('socialactions/like_box.html', takes_context=True)
def like_box(context, object_to_link, url_next):
    try:
        content = ContentType.objects.get_for_model(object_to_link)

        likes = UserAction.objects.filter(content_type=content,
                                          object_id=object_to_link.id,
                                          action_type=ActionType.LIKE).count()

        try:
            i_liked = not not UserAction.objects.filter(content_type=content,
                                            author=context['request'].user,
                                            object_id=object_to_link.id,
                                            action_type=ActionType.LIKE).get()
        except:
            i_liked = False



        try:
            i_unliked = not not UserAction.objects.filter(content_type=content,
                                            author=context['request'].user,
                                            object_id=object_to_link.id,
                                            action_type=ActionType.UNLIKE).get()
        except:
            i_unliked = False


        unlikes = UserAction.objects.filter(content_type=content,
                                          object_id=object_to_link.id,
                                          action_type=ActionType.UNLIKE).count()


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