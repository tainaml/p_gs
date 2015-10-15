from django.contrib.contenttypes.models import ContentType
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from django.utils import timezone
from apps.feed.models import FeedObject
from django.db.models import Q
from apps.socialactions.models import UserAction
from apps.socialactions.service import business as BusinessSocialActions
from rede_gsti import settings


def get_feed_objects(profile_instance=None, description=None, content_types_list=None, items_per_page=None, page=None, user=None):
    if not content_types_list:
        content_types_list = []

    followers_id = BusinessSocialActions.get_users_ids_acted_by_model_and_action(
        model=profile_instance.user,
        action=settings.SOCIAL_FOLLOW,
        user=user
    )

    content_types = ContentType.objects.filter(model__in=content_types_list)

    communities = BusinessSocialActions.get_users_acted_by_author(
        author=profile_instance.user,
        action=settings.SOCIAL_FOLLOW,
        content_type='community'
    )

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

    return feed_objects_paginated


def get_articles_from_user(profile_instance=None, description=None, content_type=None, items_per_page=None, page=None, user=None):

    feed_objects = FeedObject.objects.filter(
        Q(content_type=content_type) &
        Q(article__author=profile_instance.user) &
        (
            Q(article__title__icontains=description)|
            Q(article__text__icontains=description)
        )
    ).order_by(
        "-date"
    ).prefetch_related(
        "content_object__author"
    ).distinct(
        "object_id",
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

    return feed_objects_paginated


def get_followings(author, description=None, items_per_page=None, page=None):

    content_type = ContentType.objects.get(model="user")

    try:
        users_actions = UserAction.objects.filter(
            Q(author=author) &
            Q(action_type=settings.SOCIAL_FOLLOW) &
            Q(content_type=content_type)
        )
    except:
        users_actions = False

    return users_actions