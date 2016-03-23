# -*- coding: utf-8 -*-
from apps.account.models import User
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from django.db.models import Q
from apps.account.models import User

from apps.article.models import Article
from apps.community.models import Community
from apps.question.models import Question


def get_communities(description=None, items_per_page=None, page=None, startswith=False):

    items_per_page = items_per_page if items_per_page else 6
    page = page if page else 1

    if startswith:
        criteria = Q(title__unaccent__istartswith=description)
    else:
        criteria = None
        arr_description = description.split(' ')

        for desc in arr_description:
            query_criteria = Q(title__unaccent__icontains=desc)
            criteria = query_criteria if not criteria else criteria | query_criteria

        if len(arr_description) == 0:
            criteria = True

    communities = Community.objects.filter(criteria).distinct('id')
    communities = Paginator(communities, items_per_page)

    try:
        communities = communities.page(page)
    except PageNotAnInteger:
        communities = communities.page(1)
    except EmptyPage:
        communities = []

    return communities


def get_users(description=None, items_per_page=None, page=None, startswith=False):

    items_per_page = items_per_page if items_per_page else 6
    page = page if page else 1

    if startswith:
        criteria = (Q(first_name__unaccent__istartswith=description))
    else:
        criteria = None
        arr_description = description.split(' ')

        for desc in arr_description:
            query_criteria = (Q(first_name__unaccent__icontains=desc) |
                              Q(last_name__unaccent__icontains=desc))
            criteria = query_criteria if not criteria else criteria | query_criteria

        if len(arr_description) == 0:
            criteria = True

    users = User.objects.filter(Q(is_active=True) & Q(profile__isnull=False) & criteria).distinct('id')

    users = Paginator(users, items_per_page)
    try:
        users = users.page(page)
    except PageNotAnInteger:
        users = users.page(1)
    except EmptyPage:
        users = []

    return users


def get_articles(description=None, items_per_page=None, page=None):

    items_per_page = items_per_page if items_per_page else 6
    page = page if page else 1

    criteria = None
    arr_description = description.split(' ')

    for desc in arr_description:
        query_criteria = (Q(title__unaccent__icontains=desc) |
                          Q(text__unaccent__icontains=desc))
        criteria = query_criteria if not criteria else criteria | query_criteria

    if len(arr_description) == 0:
        criteria = True

    articles = Article.objects.filter(
        Q(status=Article.STATUS_PUBLISH) & criteria
    ).order_by('-publishin').distinct('id', 'publishin')

    articles = Paginator(articles, items_per_page)
    try:
        articles = articles.page(page)
    except PageNotAnInteger:
        articles = articles.page(1)
    except EmptyPage:
        articles = []

    return articles


def get_questions(description=None, items_per_page=None, page=None):

    items_per_page = items_per_page if items_per_page else 6
    page = page if page else 1

    criteria = None
    arr_description = description.split(' ')

    for desc in arr_description:
        query_criteria = (Q(title__unaccent__icontains=desc) |
                          Q(description__unaccent__icontains=desc))
        criteria = query_criteria if not criteria else criteria | query_criteria

    if len(arr_description) == 0:
        criteria = True

    questions = Question.objects.filter(
        Q(deleted=False) & criteria
    ).order_by('-question_date').distinct('id', 'question_date')

    questions = Paginator(questions, items_per_page)
    try:
        questions = questions.page(page)
    except PageNotAnInteger:
        questions = questions.page(1)
    except EmptyPage:
        questions = []

    return questions
