from django import template
from django.core.cache import cache

register = template.Library()


TIME_TO_CACHE = 1800

@register.inclusion_tag('community/partials/top-gamification.html', takes_context=True)
def top_community(context, community, number):
    key = "top_ranked_{0}".format(community.slug)
    top_ranked  = cache.get(key)
    if not top_ranked:

        top_ranked = community.rank.prefetch_related("user").order_by("-value")[:number]
        cache.set(key, top_ranked, TIME_TO_CACHE)


    return {
        "top_ranked": top_ranked,
        "number": number
    }




