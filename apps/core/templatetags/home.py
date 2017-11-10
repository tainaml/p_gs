from apps.community.models import Community
from apps.feed.models import ProfileStatus
from django import template
from django.contrib.auth import get_user_model

register = template.Library()


@register.inclusion_tag('userprofile/partials/join-us.html', takes_context=True)
def join_us(context, quantity):
    request = context['request']
    User = get_user_model()
    users = User.objects.filter(profile__profile_picture__isnull=False).prefetch_related("profile").order_by("?")[:quantity]
    count = User.objects.all().count()
    # Workaround
    count =  int(count / 1000) * 1000

    return {"users": users, "count": count, "request": request}


@register.inclusion_tag('home/partials/communities-slider.html')
def communities_slider():

    communities = Community.objects.all().order_by("?")

    return {"communities": communities}


@register.inclusion_tag('home/partials/commits.html')
def commits(quantity):

    commits = ProfileStatus.objects.all().prefetch_related("author").order_by("-publishin")[:quantity]

    return {"commits": commits}