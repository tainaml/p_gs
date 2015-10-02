from django.contrib.contenttypes.models import ContentType
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from apps.feed.models import FeedObject
from django.db.models import Q
from apps.socialactions.service import business as socialBusiness
from rede_gsti import settings


def get_feed_objects(profile_instance=None, description=None, content_types_list=None, items_per_page=None, page=None):

    if not content_types_list:
        content_types_list = []

    content_types = ContentType.objects.filter(model__in=content_types_list)

    communities = socialBusiness.get_users_acted_by_author(author=profile_instance.user,
                                                     action=settings.SOCIAL_FOLLOW,
                                                     content_type='community')
    taxonomy_list = []
    for community in communities:
        taxonomy_list.append(community.content_object.taxonomy)

    feed_objects = FeedObject.objects.filter(
        Q(content_type__in=content_types) &
        Q(taxonomies__in=taxonomy_list) &
        (
            Q(article__title__icontains=description) |
            Q(article__text__icontains=description)  |
            Q(question__title__icontains=description)|
            Q(question__description__icontains=description)
        )
    ).order_by(
        "-date"
    ).prefetch_related(
        "content_object__author",
        "content_object__author__profile",
        "taxonomies"
    )

    feed_objects_paginated = feed_objects
    items_per_page = items_per_page if items_per_page else 10
    page = page if page else 1

    feed_objects_paginated = Paginator(feed_objects, items_per_page)
    try:
        feed_objects_paginated = feed_objects_paginated.page(page)
    except PageNotAnInteger:
        feed_objects_paginated = feed_objects_paginated.page(1)
    except EmptyPage:
        feed_objects_paginated = []

    return feed_objects_paginated
