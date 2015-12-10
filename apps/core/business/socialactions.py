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
        raise Exception("Erro ao remover elemento")

    return UserAction.objects.filter(author=user, action_type=action_type)


def get_favourite_content(author, criteria=None, items_per_page=None, page=None):

    action_type = settings.SOCIAL_FAVOURITE

    content_type = ContentType.objects.filter(model__in=['article', 'question'])

    UserActions = UserAction.objects.filter(
        author=author,
        action_type=action_type,
        content_type=content_type
    )

    if criteria:
        articles = Article.objects.filter(
            Q(title__icontains=criteria) |
            Q(text__icontains=criteria)
        )

        UserActions = UserActions.filter(object_id__in=articles)

    items_per_page = items_per_page if items_per_page else 9
    page = page if page else 1

    items = Paginator(UserActions, items_per_page)
    try:
        items = items.page(page)
    except PageNotAnInteger:
        items = items.page(1)
    except EmptyPage:
        items = []

    return items


def remove_favourite_content(user, itens_to_remove, items_per_page=None, page=None):

    action_type = settings.SOCIAL_FAVOURITE

    try:
        for item in itens_to_remove:
            UserAction.objects.filter(author=user, action_type=action_type, id=item).delete()
    except Exception as e:
        raise Exception("Erro ao remover elemento")

    return UserAction.objects.filter(author=user, action_type=action_type)


def get_suggest_content(user, criteria=None, items_per_page=None, page=None):

    action_type = settings.SOCIAL_SUGGEST

    condition = Q(target_user=user) & Q(action_type=action_type)
    content_type = ContentType.objects.get(model='article')

    user_actions = UserAction.objects.filter(
        target_user=user,
        action_type=action_type,
        content_type=content_type
    )

    if criteria:
        articles = Article.objects.filter(
            Q(title__icontains=criteria) |
            Q(text__icontains=criteria)
        )

        user_actions = user_actions.filter(object_id__in=articles)

    items_per_page = items_per_page if items_per_page else 10
    page = page if page else 1

    feed_objects_paginated = Paginator(user_actions, items_per_page)
    try:
        feed_objects_paginated = feed_objects_paginated.page(page)
    except PageNotAnInteger:
        feed_objects_paginated = feed_objects_paginated.page(1)
    except EmptyPage:
        feed_objects_paginated = []

    return feed_objects_paginated


def remove_suggest_content(user, itens_to_remove, items_per_page=None, page=None):

    action_type = settings.SOCIAL_SUGGEST

    removed_itens = []
    try:
        for item in itens_to_remove:
            UserAction.objects.filter(target_user=user, action_type=action_type, id=item).delete()
            removed_itens.append(item)
    except Exception as e:
        raise Exception("Erro ao remover elemento")

    return removed_itens


def remove_social_actions(action_type, items_to_remove, author=None, target_user=None):

    action_allowed = [settings.SOCIAL_SUGGEST, settings.SOCIAL_FAVOURITE, settings.SOCIAL_SEE_LATER]

    if action_type not in action_allowed:
        raise Exception("Invalid action!")

    removed_items = []
    try:
        for item in items_to_remove:
            if author:
                UserAction.objects.filter(id=item.id, action_type=action_type, author=author).delete()
                removed_items.append(item.id)
            elif target_user:
                UserAction.objects.filter(id=item.id, action_type=action_type, target_user=target_user).delete()
                removed_items.append(item.id)
    except Exception:
        raise Exception("Erro ao remover elemento")

    return removed_items


def get_content_by_action(description, action_type, items_per_page=None, page=None, author=None, target_user=None):

    content_type = ContentType.objects.filter(model__in=['article', 'question'])

    criteria = Q(action_type=action_type,) & Q(content_type=content_type)

    if author:
        criteria &= Q(author=author)

    if target_user:
        criteria &= Q(target_user=target_user)

    UserActions = UserAction.objects.filter(criteria)

    if description:
        articles = Article.objects.filter(
            Q(title__icontains=description) |
            Q(text__icontains=description)
        )

        UserActions = UserActions.filter(object_id__in=articles)

    items_per_page = items_per_page if items_per_page else 9
    page = page if page else 1

    items = Paginator(UserActions, items_per_page)
    try:
        items = items.page(page)
    except PageNotAnInteger:
        items = items.page(1)
    except EmptyPage:
        items = []

    return items