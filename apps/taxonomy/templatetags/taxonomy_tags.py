from django import template
from django.contrib.contenttypes.models import ContentType
from apps.community.models import Community

from apps.feed.models import FeedObject
from apps.question.models import Question
from apps.taxonomy.models import Taxonomy

register = template.Library()

@register.inclusion_tag('taxonomy/taxonomies.html')
def taxonomies(content_object):

    content_type = ContentType.objects.get_for_model(content_object)

    communities = Community.objects.filter(
        feeds=FeedObject.objects.get(
            content_type=content_type,
            object_id=content_object.id
        )
    ).prefetch_related("taxonomy")

    return {
        'communities': communities
    }
