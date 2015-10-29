from django.contrib.contenttypes.models import ContentType
from django.db.models import Q
from apps.article.models import Article
from apps.socialactions.models import UserAction
from apps.socialactions.service.business import user_followed
from rede_gsti import settings
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage


def get_see_later_content(user, criteria=None, items_per_page=None, page=None):

    action_type = settings.SOCIAL_SEE_LATER

    condition = Q(author=user) & Q(action_type=action_type)
    content_type = ContentType.objects.filter(model='article')

    UserActions = UserAction.objects.filter(
        author=user,
        action_type=action_type,
        content_type=content_type
    )

    if criteria:
        articles = Article.objects.filter(
            Q(title__icontains=criteria) |
            Q(text__icontains=criteria)
        )

        UserActions = UserActions.filter(object_id__in=articles)

    items_per_page = items_per_page if items_per_page else 10
    page = page if page else 1

    articles_paginated = Paginator(UserActions, items_per_page)
    try:
        articles_paginated = articles_paginated.page(page)
    except PageNotAnInteger:
        articles_paginated = articles_paginated.page(1)
    except EmptyPage:
        articles_paginated = []

    return articles_paginated


def remove_see_later_content(user, itens_to_remove, items_per_page=None, page=None):

    action_type = settings.SOCIAL_SEE_LATER

    try:
        for item in itens_to_remove:
            UserAction.objects.filter(author=user, action_type=action_type, id=item).delete()
    except Exception as e:
        raise e.message("Erro ao remover elemento")

    return UserAction.objects.filter(author=user, action_type=action_type)


def get_favourite_content(user, criteria=None, items_per_page=None, page=None):

    action_type = settings.SOCIAL_FAVOURITE

    condition = Q(author=user) & Q(action_type=action_type)
    content_type = ContentType.objects.filter(model='article')

    UserActions = UserAction.objects.filter(
        author=user,
        action_type=action_type,
        content_type=content_type
    )

    if criteria:
        articles = Article.objects.filter(
            Q(title__icontains=criteria) |
            Q(text__icontains=criteria)
        )

        UserActions = UserActions.filter(object_id__in=articles)

    items_per_page = items_per_page if items_per_page else 10
    page = page if page else 1

    articles_paginated = Paginator(UserActions, items_per_page)
    try:
        articles_paginated = articles_paginated.page(page)
    except PageNotAnInteger:
        articles_paginated = articles_paginated.page(1)
    except EmptyPage:
        articles_paginated = []

    return articles_paginated


def remove_favourite_content(user, itens_to_remove, items_per_page=None, page=None):

    action_type = settings.SOCIAL_FAVOURITE

    try:
        for item in itens_to_remove:
            UserAction.objects.filter(author=user, action_type=action_type, id=item).delete()
    except Exception as e:
        raise e.message("Erro ao remover elemento")

    return UserAction.objects.filter(author=user, action_type=action_type)


def get_suggest_content(user, criteria=None, items_per_page=None, page=None):

    action_type = settings.SOCIAL_SUGGEST

    # is_friend(user, user)

    condition = Q(author=user) & Q(action_type=action_type)
    content_type = ContentType.objects.filter(model='article')

    UserActions = UserAction.objects.filter(
        author=user,
        action_type=action_type,
        content_type=content_type
    )

    if criteria:
        articles = Article.objects.filter(
            Q(title__icontains=criteria) |
            Q(text__icontains=criteria)
        )

        UserActions = UserActions.filter(object_id__in=articles)

    items_per_page = items_per_page if items_per_page else 10
    page = page if page else 1

    articles_paginated = Paginator(UserActions, items_per_page)
    try:
        articles_paginated = articles_paginated.page(page)
    except PageNotAnInteger:
        articles_paginated = articles_paginated.page(1)
    except EmptyPage:
        articles_paginated = []

    return articles_paginated


def remove_suggest_content(user, itens_to_remove, items_per_page=None, page=None):

    action_type = settings.SOCIAL_SUGGEST

    try:
        for item in itens_to_remove:
            UserAction.objects.filter(author=user, action_type=action_type, id=item).delete()
    except Exception as e:
        raise e.message("Erro ao remover elemento")

    return UserAction.objects.filter(author=user, action_type=action_type)


# If one user folow another user and that user folow back the author user, they're friends.
# def is_friend(author, target):

    # user_acted_by_object()
    # users = user_followed(author)
    # for _user in users:
    #     print _user