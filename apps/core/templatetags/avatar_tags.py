from django import template
from django.conf import settings
from django.contrib.auth import get_user_model
from django_thumbor import generate_url

register = template.Library()


def get_avatar_path(gender):
    return settings.AVATAR[gender]


@register.simple_tag(takes_context=True)
def get_avatar(context, user, **kwargs):
    UserModel = get_user_model()
    request = context.get('request')

    user_profile = None
    try:
        user_profile = user.user_profile
    except Exception:
        pass

    if not isinstance(user, UserModel):
        image_url = get_avatar_path('M')
        return generate_url(image_url, **kwargs)


    if request and (user.is_active or (request.user == user and request.user.is_authenticated())):

        if user_profile and user_profile.profile_picture and user_profile.profile_picture.name:
            image_url = '%s/%s' % (settings.THUMBOR_MEDIA_URL, user_profile.profile_picture.name)
        else:
            image_url = get_avatar_path(user_profile.gender if user_profile and user_profile.gender else 'M')
    elif not user.is_active:
        image_url = get_avatar_path(user_profile.gender if user_profile and user_profile.gender else 'M')
    else:
        image_url = get_avatar_path('M')

    return generate_url(image_url, **kwargs)
