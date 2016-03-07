from django import template
from django.conf import settings
from django_thumbor import generate_url

register = template.Library()


def get_avatar_path(gender):
    return settings.AVATAR[gender]


@register.simple_tag
def get_avatar(user, **kwargs):

    if user.is_authenticated():
        if user.profile and user.profile.profile_picture and user.profile.profile_picture.name:
            image_url = '%s/%s' % (settings.THUMBOR_MEDIA_URL, user.profile.profile_picture.name)
        else:
            image_url = get_avatar_path(user.profile.gender if user.profile.gender else 'M')
    else:
        image_url = get_avatar_path('M')
    return generate_url(image_url, **kwargs)
