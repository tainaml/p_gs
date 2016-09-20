from django import template
from django.contrib.contenttypes.models import ContentType

from apps.community.models import Community
from apps.core.business.content_types import ContentTypeCached
from apps.feed.models import FeedObject

register = template.Library()

@register.inclusion_tag('taxonomy/taxonomies.html')
def taxonomies(content_object):

    content_type = ContentTypeCached.objects.get_for_model(content_object)

    try:
        feed = FeedObject.objects.get(
            content_type=content_type,
            object_id=content_object.id
        )

        communities = Community.objects.filter(
            feeds=feed
        ).prefetch_related("taxonomy")
    except:
        communities = []

    return {
        'communities': communities
    }
