from django import template
from django.contrib.auth import get_user_model

register = template.Library()


@register.inclusion_tag('userprofile/partials/join-us.html', takes_context=True)
def join_us(context, quantity):
    request = context['request']
    User = get_user_model()
    users = User.objects.filter(profile__profile_picture__isnull=False).prefetch_related("profile").order_by("?")[:quantity]
    count = User.objects.all().count()

    return {"users": users, "count": count, "request": request}