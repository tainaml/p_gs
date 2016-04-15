from django import template
from django.core.cache import cache

from apps.community.models import Community
from apps.taxonomy.service.business import get_related_list_top_down

register = template.Library()

# cache = caches['default']


@register.inclusion_tag('core/templatetags/communities-related.html', takes_context=True)
def communities_related(context, category, count=5):

    if not category:
        return

    count = 5 if count > 10 else count

    cache_prefix = 'cached_communities_related_'
    cache_key = "{cache_prefix}{category_slug}".format(
        cache_prefix=cache_prefix,
        category_slug=category.slug
    )

    communities = cache.get(cache_key, [])

    if not communities:
        taxonomies = get_related_list_top_down([category])
        communities = Community.objects.filter(taxonomy__in=taxonomies).exclude(taxonomy=category).order_by('?')[:count]
        cache.set(cache_key, communities, 60 * 60)

    response_data = {
        'communities': communities,
        'request': context.get('request')
    }

    return response_data
