# -*- coding: utf-8 -*-
from django.conf import settings
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from django.db.models import Q
from apps.article.models import Article
from apps.community.models import Community
from apps.question.models import Question
from apps.userprofile.models import UserProfile
from itertools import chain
from collections import OrderedDict


def get_communities(description=None, items_per_page=None, page=None, startswith=False, category=None):

    items_per_page = items_per_page if items_per_page else 6
    page = page if page else 1

    if startswith:
        criteria = Q(title__unaccent__istartswith=description)
    else:
        criteria = None
        arr_description = description.split(' ')

        for desc in arr_description:
            if desc != u'None':
                query_criteria = Q(title__unaccent__icontains=desc)
            else:
                query_criteria = Q(1==1)

            criteria = query_criteria if criteria is None else criteria | query_criteria

        if len(arr_description) == 0:
            criteria = True

    if category:
        category_cryteria = Q(taxonomy__parent__slug=category)
        criteria = category_cryteria if not criteria else criteria & category_cryteria

    communities = Community.objects.filter(criteria).order_by('title').distinct('title')
    communities = Paginator(communities, items_per_page)

    try:
        communities = communities.page(page)
    except PageNotAnInteger:

        communities = communities.page(1)
    except EmptyPage:
        communities = []

    return communities


def get_users(description=None, items_per_page=None, page=None, startswith=False, state=None, city=None):

    items_per_page = items_per_page if items_per_page else 6
    page = page if page else 1

    if startswith:
        criteria = (Q(user__first_name__unaccent__istartswith=description))
    else:
        criteria = None
        arr_description = description.split(' ')

        for desc in arr_description:
            query_criteria = (Q(user__first_name__unaccent__icontains=desc) |
                              Q(user__last_name__unaccent__icontains=desc))
            criteria = query_criteria if not criteria else criteria | query_criteria

        if len(arr_description) == 0:
            criteria = True

    if state:
        state_criteria = Q(user__profile__city__state=state)
        criteria = state_criteria if not criteria else criteria & state_criteria

    if city:
        city_criteria = Q(user__profile__city=city)
        criteria = city_criteria if not criteria else criteria & city_criteria

    # TODO remove empty register
    exclude_empty_register = ~Q(user__username__exact='') and Q(wizard_step__gte=getattr(settings, 'WIZARD_STEPS_TOTAL'))

    userprofiles = UserProfile.objects.filter(Q(user__is_active=True) & exclude_empty_register & criteria).distinct('id')

    users = []

    for profile in userprofiles:
        users.append(profile.user)

    users = Paginator(users, items_per_page)
    try:
        users = users.page(page)
    except PageNotAnInteger:
        users = users.page(1)
    except EmptyPage:
        users = []

    return users


def get_articles_by_title(arr_description):
    criteria = None

    for desc in arr_description:
        title_criteria = Q(title__unaccent__icontains=desc)
        criteria = title_criteria if not criteria else criteria & title_criteria

    if len(arr_description) == 0:
        criteria = True

    articles = Article.objects.filter(
        Q(status=Article.STATUS_PUBLISH) & criteria
    ).order_by('-publishin').distinct('id', 'publishin')

    return articles


def get_articles_by_description(arr_description):
    criteria = None

    for desc in arr_description:
        title_criteria = Q(text__unaccent__icontains=desc)
        criteria = title_criteria if not criteria else criteria & title_criteria

    if len(arr_description) == 0:
        criteria = True

    articles = Article.objects.filter(
        Q(status=Article.STATUS_PUBLISH) & criteria
    ).order_by('-publishin').distinct('id', 'publishin')

    return articles


def get_articles_general(arr_description):
    criteria = None

    for desc in arr_description:
        query_criteria = (Q(title__unaccent__icontains=desc) |
                          Q(text__unaccent__icontains=desc))
        criteria = query_criteria if not criteria else criteria | query_criteria

    if len(arr_description) == 0:
        criteria = True

    articles = Article.objects.filter(
        Q(status=Article.STATUS_PUBLISH) & criteria
    ).order_by('-publishin').distinct('id', 'publishin')

    return articles


def get_articles(description=None, items_per_page=None, page=None):

    items_per_page = items_per_page if items_per_page else 6
    page = page if page else 1

    arr_description = description.split(' ')

    articles_by_title = get_articles_by_title(arr_description)

    articles_by_description = get_articles_by_description(arr_description)

    articles_general = get_articles_general(arr_description)

    articles = list(OrderedDict.fromkeys(chain(articles_by_title, articles_by_description, articles_general)))

    articles = Paginator(articles, items_per_page)
    try:
        articles = articles.page(page)
    except PageNotAnInteger:
        articles = articles.page(1)
    except EmptyPage:
        articles = []

    return articles


def get_questions_by_title(arr_description):
    criteria = None

    for desc in arr_description:
        query_criteria = Q(title__unaccent__icontains=desc)
        criteria = query_criteria if not criteria else criteria & query_criteria

    if len(arr_description) == 0:
        criteria = True

    questions = Question.objects.filter(
        Q(deleted=False) & criteria
    ).order_by('-question_date').distinct('id', 'question_date')

    return questions


def get_questions_by_description(arr_description):
    criteria = None

    for desc in arr_description:
        query_criteria = Q(description__unaccent__icontains=desc)
        criteria = query_criteria if not criteria else criteria & query_criteria

    if len(arr_description) == 0:
        criteria = True

    questions = Question.objects.filter(
        Q(deleted=False) & criteria
    ).order_by('-question_date').distinct('id', 'question_date')

    return questions


def get_questions_general(arr_description):
    criteria = None

    for desc in arr_description:
        query_criteria = (Q(title__unaccent__icontains=desc) |
                          Q(description__unaccent__icontains=desc))
        criteria = query_criteria if not criteria else criteria | query_criteria

    if len(arr_description) == 0:
        criteria = True

    questions = Question.objects.filter(
        Q(deleted=False) & criteria
    ).order_by('-question_date').distinct('id', 'question_date')

    return questions


def get_questions(description=None, items_per_page=None, page=None):

    items_per_page = items_per_page if items_per_page else 6
    page = page if page else 1

    arr_description = description.split(' ')

    questions_by_title = get_questions_by_title(arr_description)

    questions_by_description = get_questions_by_description(arr_description)

    questions_general = get_questions_general(arr_description)

    questions = list(OrderedDict.fromkeys(chain(questions_by_title, questions_by_description, questions_general)))

    questions = Paginator(questions, items_per_page)
    try:
        questions = questions.page(page)
    except PageNotAnInteger:
        questions = questions.page(1)
    except EmptyPage:
        questions = []

    return questions
