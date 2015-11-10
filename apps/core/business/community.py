from django.contrib.contenttypes.models import ContentType
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from django.db.models import Q
from apps.article.models import Article

from apps.community.models import Community
from apps.core.models.embed import EmbedItem
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


def get_communities(taxonomies_list=None, description=None, items_per_page=None, page=None):

    items_per_page = items_per_page if items_per_page else 9
    page = page if page else 1

    communities = Community.objects.filter(
        Q(taxonomy__in=taxonomies_list) &
        (
            Q(title__icontains=description) |
            Q(description__icontains=description)
        )
    )

    if items_per_page and page:
        communities = Paginator(communities, items_per_page)
        try:
            communities = communities.page(page)
        except PageNotAnInteger:
            communities = communities.page(1)
        except EmptyPage:
            communities = []

    return communities


def get_articles_with_videos(community, description=None, items_per_page=None, page=None):

    content_type = ContentType.objects.filter(model="article")

    feed_objects = FeedObject.objects.filter(
        Q(content_type=content_type) &
        Q(taxonomies=community.taxonomy) &
        (
            Q(article__title__icontains=description) |
            Q(article__text__icontains=description)
        )
    )

    posts_videos = Article.objects.filter(
        Q(embed__embed_type=EmbedItem.TYPE_VIDEO) &
        Q(status=Article.STATUS_PUBLISH) &
        (
            Q(title__icontains=description) |
            Q(text__icontains=description)
        )
    )

    posts = feed_objects.filter(
        Q(content_type=content_type) &
        Q(object_id__in=posts_videos)
    )

    items_per_page = items_per_page if items_per_page else 10
    page = page if page else 1

    if items_per_page and page:
        posts = Paginator(posts, items_per_page)
        try:
            posts = posts.page(page)
        except PageNotAnInteger:
            posts = posts.page(1)
        except EmptyPage:
            posts = []

    return posts


def get_random_communities_by_article_or_question(object_id=None, content_type=None):

    content_type = ContentType.objects.get(model=content_type)

    feed = FeedObject.objects.get(
        object_id=object_id,
        content_type=content_type
    )

    communities = feed.communities.all().order_by('?')

    return communities