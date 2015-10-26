from apps.socialactions.models import UserAction
from rede_gsti import settings
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage


def get_see_later_content(user, items_per_page=None, page=None):

    action_type = settings.SOCIAL_SEE_LATER
    articles = UserAction.objects.filter(author=user, action_type=action_type)

    items_per_page = items_per_page if items_per_page else 10
    page = page if page else 1

    articles_paginated = Paginator(articles, items_per_page)
    try:
        articles_paginated = articles_paginated.page(page)
    except PageNotAnInteger:
        articles_paginated = articles_paginated.page(1)
    except EmptyPage:
        articles_paginated = []

    return articles_paginated


def remove_see_later_content(user, itens_to_remove, items_per_page=None, page=None):

    action_type = settings.SOCIAL_SEE_LATER

    articles = UserAction.objects.filter(author=user, action_type=action_type)

    try:
        for itens in itens_to_remove:
            UserAction.objects.filter(author=user, action_type=action_type, id=itens).delete()
    except Exception as e:
        raise e.message("Erro ao remover elemento")
