from django.contrib.contenttypes.models import ContentType
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from django.utils import timezone
from apps.feed.models import FeedObject
from django.db.models import Q
from apps.socialactions.service import business as socialBusiness
from rede_gsti import settings


def get_feed_objects(profile_instance=None, description=None, content_types_list=None, items_per_page=None, page=None, user=None):
    print timezone.now()
    if not content_types_list:
        content_types_list = []

    followers_id = socialBusiness.get_users_ids_acted_by_model_and_action(model=profile_instance.user,
                                                          action=settings.SOCIAL_FOLLOW,
                                                          user=user
                                                      )

    content_types = ContentType.objects.filter(model__in=content_types_list)

    communities = socialBusiness.get_users_acted_by_author(author=profile_instance.user,
                                                     action=settings.SOCIAL_FOLLOW,
                                                     content_type='community')
    taxonomy_list = []
    for community in communities:
        taxonomy_list.append(community.content_object.taxonomy)

    feed_objects = FeedObject.objects.filter(
        Q(content_type__in=content_types) &
        (
            Q(taxonomies__in=taxonomy_list) |
            Q(article__author__in=followers_id) |
            Q(question__author__in=followers_id)
        )
    ).order_by(
        "-date"
    ).prefetch_related(
        "content_object__author",
        "content_object__author__profile",
        "taxonomies"
    ).distinct(
        "object_id",
        "content_type",
        "date"
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
    print timezone.now()
    return feed_objects_paginated
