from django.contrib.contenttypes.models import ContentType
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from django.db.models import Q

from apps.article.models import Article
from apps.community.models import Community
from apps.core.models.embed import EmbedItem
from apps.feed.models import FeedObject
from apps.socialactions.models import UserAction
from rede_gsti import settings
from apps.taxonomy.models import Taxonomy

__author__ = 'phillip'

def get_feed_objects(community_instance=None, description=None, content_types_list=None, items_per_page=None, page=None, official=None):

    if not content_types_list:
        content_types_list = []

    content_types = ContentType.objects.filter(model__in=content_types_list)

    feed_objects = FeedObject.objects.filter(
        Q(content_type__in=content_types) &
        Q(communities=community_instance) &
        (
            (
                Q(article__status=Article.STATUS_PUBLISH) &
                (
                    Q(article__title__icontains=description) |
                    Q(article__text__icontains=description)
                )
            ) |
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

    if official is True:
        feed_objects = feed_objects.filter(official=official)

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
        Q(taxonomy__in=taxonomies_list)
        &Q(title__icontains=description)

    ).order_by("id")
    if description:
        communities.filter(Q(title__icontains=description))

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


def get_followers(data=None, items_per_page=None, page=None, startswith=None):

    community = data.get('community')
    content_type = ContentType.objects.get_for_model(community)

    criteria = (
        Q(content_type=content_type) &
        Q(object_id=community.id) &
        Q(action_type=settings.SOCIAL_FOLLOW)
    )

    if data.get('criteria'):
        criteria = criteria & (
            (
                Q(author__first_name__icontains=data.get('criteria')) |
                Q(author__last_name__icontains=data.get('criteria'))
            )
        )

    if data.get('state'):
        criteria = criteria & (Q(author__profile__city__state=data.get('state')))

    if data.get('city'):
        criteria = criteria & (Q(author__profile__city=data.get('city')))

    try:
        followers = UserAction.objects.filter(criteria)
    except ValueError:
        return False

    items_per_page = items_per_page if items_per_page else 6
    page = page if page else 1

    if items_per_page and page:
        followers = Paginator(followers, items_per_page)
        try:
            followers = followers.page(page)
        except PageNotAnInteger:
            followers = followers.page(1)
        except EmptyPage:
            followers = []

    return followers


# @TODO refactor
def get_related_communities(community_slug):

    try:

        community = Community.objects.get(slug=community_slug)

        community_tax = Taxonomy.objects.get(id=community.taxonomy.id)
        children = Taxonomy.objects.filter(parent_id=community_tax.id)
        parent = Taxonomy.objects.filter(id=community_tax.parent_id)

        communities = Community.objects.filter(
            Q(taxonomy_id__in=children) |
            Q(taxonomy_id__in=parent)
        )

    except Community.DoesNotExist:
        return []

    return communities