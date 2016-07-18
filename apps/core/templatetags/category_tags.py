from django import template

from apps.community.models import Community
from apps.taxonomy.service.business import get_related_list_top_down

register = template.Library()


@register.inclusion_tag('core/templatetags/communities-related.html', takes_context=True)
def communities_related(context, category, count=5):

    if not category:
        return

    count = 5 if count > 10 else count

    taxonomies = get_related_list_top_down([category])
    communities = Community.objects.filter(taxonomy__in=taxonomies).exclude(taxonomy=category).order_by('?')[:count]

    response_data = {
        'communities': communities,
        'category': category,
        'request': context.get('request')
    }

    return response_data
