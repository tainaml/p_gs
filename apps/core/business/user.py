from apps.userprofile.models import UserProfile
from django.contrib.auth import get_user_model
from django.contrib.postgres.search import SearchQuery, SearchRank
from apps.core.business import search as SearchBusiness
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from django_thumbor import generate_url
from django.db.models import Q
from django.conf import settings

from apps.account.models import User
from apps.community.models import Community
from apps.article.models import Article
from apps.core.business.content_types import ContentTypeCached
from apps.core.business.search import get_articles_feed_queryset, get_question_feed_queryset
from apps.core.models.embed import EmbedItem
from apps.feed.models import FeedObject
from apps.question.models import Question
from apps.socialactions.models import UserAction
from apps.socialactions.service import business as BusinessSocialActions


User = get_user_model()


def get_user_communities(author):
    user_communities = BusinessSocialActions.get_users_acted_by_author(
        author=author,
        action=settings.SOCIAL_FOLLOW,
        content_type='community',
        items_per_page=None,
    )

    community_ids = []
    for action in user_communities:
        community_ids.append(action.content_object.id)

    communities = Community.objects.filter(pk__in=community_ids)

    return communities


def get_user_communities_list_from_queryset(queryset, author, width=20, height=20, id_field='id'):
    communities = []

    for community in queryset:
        img_url = str(settings.THUMBOR_MEDIA_URL) + '/' + str(community.image)

        c = dict()
        c['id'] = getattr(community, id_field)
        c['name'] = community.title
        c['image'] = generate_url(img_url, width=width, height=height, thumbor_server=settings.THUMBOR_SERVER)

        communities.append(c)

    return communities

def get_user_communities_list(author, width=20, height=20):

    communities_queryset = get_user_communities(author)
    return get_user_communities_list_from_queryset(communities_queryset, author, width, height)


def get_feed_objects(profile_instance=None, description=None, content_types_list=None, items_per_page=None, page=None, user=None):

    if not content_types_list:
        content_types_list = []

    content_types = ContentTypeCached.objects.filter(model__in=content_types_list)

    followers_id = BusinessSocialActions.get_users_ids_acted_by_model_and_action(
        model=None,
        action=settings.SOCIAL_FOLLOW,
        user=user
    )

    community_list = BusinessSocialActions.get_user_communities_following(
        author=profile_instance.user,
    )

    feed_objects = FeedObject.objects.filter(
        Q(content_type__in=content_types) &
        (
            Q(article__status=Article.STATUS_PUBLISH) |
            Q(question__deleted=False)
        ) &
        (
            Q(communities__id__in=community_list) |
            Q(article__author__in=followers_id) |
            Q(question__author__in=followers_id)
        )
    ).prefetch_related(
        "content_object",
        "content_object__author",
        "content_type",
        "communities",
        "communities__taxonomy"
    ).select_related('content_type')

    feed_objects = feed_objects.order_by(
        "-date"
    ).distinct()

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


    # if not content_types_list:
    #     content_types_list = []
    #
    # followers_id = BusinessSocialActions.get_users_ids_acted_by_model_and_action(
    #     model=None,
    #     action=settings.SOCIAL_FOLLOW,
    #     user=user
    # )
    #
    # content_types = ContentTypeCached.objects.filter(model__in=content_types_list)
    #
    # communities = BusinessSocialActions.get_users_acted_by_author(
    #     author=profile_instance.user,
    #     action=settings.SOCIAL_FOLLOW,
    #     content_type='community'
    # )
    #
    # taxonomy_list = []
    # community_list = []
    # for community in communities:
    #     taxonomy_list.append(community.content_object.taxonomy)
    #     community_list.append(community.content_object)
    #
    # feed_objects = FeedObject.objects.filter(
    #     Q(content_type__in=content_types) &
    #     (
    #         Q(article__status=Article.STATUS_PUBLISH) |
    #         Q(question__deleted=False)
    #     ) &
    #     (
    #         Q(communities__in=community_list) |
    #         Q(article__author__in=followers_id) |
    #         Q(question__author__in=followers_id)
    #     )
    # ).order_by(
    #     "-date"
    # ).prefetch_related(
    #     "content_object__author",
    #     "content_object__author__profile",
    #     "communities"
    # ).distinct(
    #     "object_id",
    #     "content_type",
    #     "date"
    # )
    #
    # items_per_page = items_per_page if items_per_page else 10
    # page = page if page else 1
    #
    # feed_objects_paginated = Paginator(feed_objects, items_per_page)
    # try:
    #     feed_objects_paginated = feed_objects_paginated.page(page)
    # except PageNotAnInteger:
    #     feed_objects_paginated = feed_objects_paginated.page(1)
    # except EmptyPage:
    #     feed_objects_paginated = []
    #
    # return feed_objects_paginated


def get_articles_from_user(profile_instance=None, description=None, content_type=None, items_per_page=None, page=None, user=None):

    feed_objects = get_articles_feed_queryset(description)
    feed_objects = feed_objects.filter(article__author=profile_instance.user)

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


def get_questions_from_user(profile_instance=None, description=None, content_type=None, items_per_page=None, page=None, user=None):

    feed_objects = get_question_feed_queryset(description)
    feed_objects = feed_objects.filter(question__author=profile_instance.user)

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


def get_active_articles_from_user(profile_instance=None, description=None, content_type=None, items_per_page=None, page=None, user=None):

    feed_objects = FeedObject.objects.filter(
        Q(content_type=content_type) &
        Q(article__author=profile_instance.user) &
        Q(article__status=Article.STATUS_PUBLISH) &
        Q(article__slug__isnull=False) &
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



def get_feed_articles(author, description=None, status=None, items_per_page=None, page=None, order=None):

    __articles = SearchBusiness.get_articles_general_feed_queryset(description)

    status = [status] if status else Article.STATUS_ALL

    content_type = ContentTypeCached.objects.get(model='article')
    query = SearchQuery(description)
    feed_objects = FeedObject.objects.filter(
        Q(content_type=content_type)
        & Q(id__in=__articles)
        & Q(article__author=author)
        & Q(article__status__in=status)
    ).annotate(
        rank=SearchRank(Article.VECTOR, query)
    ).prefetch_related(
        "content_object",
        "content_object__author",
        "content_type",
        "communities",
        "communities__taxonomy").distinct("id", "date").order_by("-date")

    items_per_page = items_per_page if items_per_page else 10
    page = page if page else 1

    if items_per_page and page:
        feed_objects = Paginator(feed_objects, items_per_page)
        try:
            feed_objects = feed_objects.page(page)
        except PageNotAnInteger:
            feed_objects = feed_objects.page(1)
        except EmptyPage:
            feed_objects = []

    return feed_objects


def get_articles_with_videos(author, description=None, items_per_page=None, page=None):

    posts = EmbedItem.objects.filter(
        Q(embed_type=EmbedItem.TYPE_VIDEO) &
        Q(article__author=author) &
        Q(article__status=Article.STATUS_PUBLISH) &
        (
            Q(article__title__icontains=description) |
            Q(article__text__icontains=description)
        )
    ).prefetch_related("content_object__author")

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


def get_questions(author, description=None, deleted=None, items_per_page=None, page=None):

    condition = Q(author=author) & (Q(title__unaccent__icontains=description) |
                                    Q(description__unaccent__icontains=description))

    if deleted is not None:
        condition &= Q(deleted=deleted)

    questions = Question.objects.filter(condition).prefetch_related("author").order_by('-question_date')

    items_per_page = items_per_page if items_per_page else 10
    page = page if page else 1

    if items_per_page and page:
        questions = Paginator(questions, items_per_page)

        try:
            questions = questions.page(page)
        except PageNotAnInteger:
            questions = questions.page(1)
        except EmptyPage:
            questions = []

    return questions


def get_followings(author, description=None, items_per_page=None, page=None):

    content_type = ContentTypeCached.objects.get(model="user")

    if description:
        strings = description.strip().split(' ')
        condition = (
            Q(first_name__icontains=strings[0].strip()) |
            Q(last_name__icontains=strings[0].strip())
        )
        for string in strings[1:]:
            condition |= (
                Q(first_name__icontains=string.strip()) |
                Q(last_name__icontains=string.strip())
            )
    else:
        condition = True

    try:
        users_filter = User.objects.filter(Q(is_active=True) & condition)

        users_followers = UserAction.objects.filter(
            Q(author=author) &
            Q(action_type=settings.SOCIAL_FOLLOW) &
            Q(content_type=content_type)
        )

        users_actions = users_followers.filter(object_id__in=users_filter)
    except:
        users_actions = False

    if items_per_page and page:
        users_actions = Paginator(users_actions, items_per_page)
        try:
            users_actions = users_actions.page(page)
        except PageNotAnInteger:
            users_actions = users_actions.page(1)
        except EmptyPage:
            users_actions = []

    return {
        'items': users_actions,
        'content_type': content_type,
        'object': author
    }


def get_all_followers(user_filter, description=None, content_type=None):

    if not content_type:
        content_type = ContentTypeCached.objects.get(model=user_filter)

    strings = description.strip().split(' ')

    condition = (
        Q(author__first_name__icontains=strings[0].strip()) |
        Q(author__last_name__icontains=strings[0].strip())
    )
    for string in strings[1:]:
        condition |= (
            Q(author__first_name__icontains=string.strip()) |
            Q(author__last_name__icontains=string.strip())
        )

    try:
        users_actions = UserAction.objects.filter(
            Q(action_type=settings.SOCIAL_FOLLOW) &
            Q(content_type=content_type) &
            Q(object_id=user_filter.id) & condition
        )
    except:
        users_actions = False

    return users_actions


def get_followers(user_filter, description=None, items_per_page=None, page=None):

    content_type = ContentTypeCached.objects.get(model=user_filter)

    users_actions = get_all_followers(user_filter, description, content_type)
    users_actions = Paginator(users_actions, items_per_page)

    try:
        users_actions = users_actions.page(page)
    except PageNotAnInteger:
        users_actions = users_actions.page(1)
    except EmptyPage:
        users_actions = []

    return {
        'items': users_actions,
        'content_type': content_type,
        'object': user_filter
    }

def get_active_users():
    return UserProfile.objects.filter(
        user__is_active=True,
        wizard_step__gte=settings.WIZARD_STEPS_TOTAL
    )