from django.contrib.contenttypes.models import ContentType
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from django.db.models import Q
from apps.feed.models import FeedObject

__author__ = 'phillip'

def get_feed_objects(community_instance=None, description=None, content_types_list=None, items_per_page=None, page=None):

    if not content_types_list:
        content_types_list = []

    content_types = ContentType.objects.filter(model__in=content_types_list)

    feed_objects = FeedObject.objects.filter(
        Q(content_type__in=content_types) &
        Q(taxonomies=community_instance.taxonomy) &
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


def get_feed_questions(community_instance=None, description=None, content_types_list=None, replies=None, items_per_page=None, page=None):

    if not content_types_list:
        content_types_list = []

    content_types = ContentType.objects.filter(model__in=content_types_list)

    if replies == 'reply':
        criteria = (
            Q(content_type__in=content_types) &
            Q(taxonomies=community_instance.taxonomy) &
            (
                Q(question__title__icontains=description) |
                Q(question__description__icontains=description)
            ) &
            Q(question__question_owner__isnull=False)
        )
    elif replies == 'non-reply':
        criteria = (
            Q(content_type__in=content_types) &
            Q(taxonomies=community_instance.taxonomy) &
            (
                Q(question__title__icontains=description) |
                Q(question__description__icontains=description)
            ) &
            Q(question__question_owner__isnull=True)
        )
    else:
        criteria = (
            Q(content_type__in=content_types) &
            Q(taxonomies=community_instance.taxonomy) &
            (
                Q(question__title__icontains=description) |
                Q(question__description__icontains=description)
            )
        )

    feed_objects = FeedObject.objects.filter(criteria).order_by("-date").prefetch_related(
        "content_object__author",
        "content_object__author__profile",
        "taxonomies"
    )

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