from django import template
from django.conf import settings
from django_thumbor import generate_url

register = template.Library()


def get_avatar_path(gender):
    return settings.AVATAR[gender]


@register.simple_tag(takes_context=True)
def get_avatar(context, user, **kwargs):

    request = context.get('request')

    if user.is_active or (request.user == user and request.user.is_authenticated()):
        if user.profile and user.profile.profile_picture and user.profile.profile_picture.name:
            image_url = '%s/%s' % (settings.THUMBOR_MEDIA_URL, user.profile.profile_picture.name)
        else:
            image_url = get_avatar_path(user.profile.gender if user.profile.gender else 'M')
    elif not user.is_active:
        image_url = get_avatar_path(user.profile.gender if user.profile.gender else 'M')
    else:
        image_url = get_avatar_path('M')

    return generate_url(image_url, **kwargs)
