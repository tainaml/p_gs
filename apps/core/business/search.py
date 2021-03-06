# -*- coding: utf-8 -*-
from django.conf import settings
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from django.db.models import Q
from apps.account.models import User
from apps.article.models import Article
from apps.community.models import Community
from apps.feed.models import FeedObject, ProfileStatus
from apps.question.models import Question
from django.contrib.postgres.search import  SearchQuery, SearchRank


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
                #What?? Why??
                query_criteria = Q(1==1)

            criteria = query_criteria if criteria is None else criteria | query_criteria

        if len(arr_description) == 0:
            criteria = True

    if category:
        category_cryteria = Q(taxonomy__parent__slug=category)
        criteria = category_cryteria if not criteria else criteria & category_cryteria

    communities = Community.objects.filter(criteria).order_by('title').prefetch_related("taxonomy", "taxonomy__parent").distinct('title')
    communities = Paginator(communities, items_per_page)

    try:
        communities = communities.page(page)
    except PageNotAnInteger:

        communities = communities.page(1)
    except EmptyPage:
        communities = []

    return communities


def get_users(description=None, items_per_page=None, page=None, startswith=False, state=None, city=None, responsibility=None):

    items_per_page = items_per_page if items_per_page else 6
    page = page if page else 1

    terms = description.split(' ')
    if startswith:
        has_more_than_one_term = len(terms) > 1

        if has_more_than_one_term:

            #TODO refactor this ugly queries
            first_term = terms[0]
            last_term = terms[1]
            full_term_criteria = Q(first_name__unaccent__istartswith=first_term) & Q(last_name__unaccent__istartswith=last_term)

            exists_users_with_full_term = User.objects.filter(full_term_criteria).exists()
            if exists_users_with_full_term:
                criteria = full_term_criteria
            else:
                criteria = (Q(first_name__unaccent__istartswith=description) | Q(last_name__unaccent__istartswith=description))
                for term in terms:
                    term_criteria = (Q(first_name__unaccent__icontains=term) | Q(last_name__unaccent__icontains=term))
                    criteria = criteria | term_criteria if criteria else term_criteria


        else:
            criteria = (Q(first_name__unaccent__istartswith=description) | Q(last_name__unaccent__istartswith=description))



    else:
        criteria = None
        arr_description = description.split(' ')

        for desc in arr_description:
            query_criteria = (Q(first_name__unaccent__icontains=desc) |
                              Q(last_name__unaccent__icontains=desc))
            criteria = query_criteria if not criteria else criteria | query_criteria

        if len(arr_description) == 0:
            criteria = True

    if state:
        state_criteria = Q(profile__city_hometown__state=state)
        criteria = state_criteria if not criteria else criteria & state_criteria

    if city:
        city_criteria = Q(profile__city_hometown=city)
        criteria = city_criteria if not criteria else criteria & city_criteria

    if responsibility:
        responsibility_criteria = Q(profile__occupation__responsibility=responsibility)
        criteria = responsibility_criteria if not criteria else criteria & responsibility_criteria

    # TODO remove empty register
    exclude_empty_register = ~Q(username__exact='') and Q(profile__wizard_step__gte=getattr(settings, 'WIZARD_STEPS_TOTAL'))

    users = User.objects.filter(Q(is_active=True) & criteria & exclude_empty_register).prefetch_related("profile").distinct('id')


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
    criteria_base = Q(status=Article.STATUS_PUBLISH)

    for desc in arr_description:
        title_criteria = Q(title__unaccent__icontains=desc)
        criteria = title_criteria if not criteria else criteria & title_criteria

    if criteria:
        criteria_base &= criteria

    articles = Article.objects.filter(
        criteria_base
    ).order_by('-publishin').distinct('id', 'publishin')

    return articles


def get_articles_by_description(arr_description):
    criteria = None
    criteria_base = Q(status=Article.STATUS_PUBLISH)

    for desc in arr_description:
        title_criteria = Q(text__unaccent__icontains=desc)
        criteria = title_criteria if not criteria else criteria & title_criteria

    if criteria:
        criteria_base &= criteria

    articles = Article.objects.filter(
        criteria_base
    ).order_by('-publishin').distinct('id', 'publishin')

    return articles


def get_articles_general(arr_description):

    criteria = None
    criteria_base = Q(status=Article.STATUS_PUBLISH)

    for desc in arr_description:
        query_criteria = (Q(title__unaccent__icontains=desc) |
                          Q(text__unaccent__icontains=desc))
        criteria = query_criteria if not criteria else criteria | query_criteria


    if criteria:
        criteria_base &= criteria

    articles = Article.objects.filter(
         criteria_base
    ).order_by('-publishin').distinct('id', 'publishin')

    return articles


def get_feed_articles(description):

    arr_description = []
    has_description = len(description.split())

    arr_description = description.split(' ') if has_description else arr_description
    articles_by_title = get_articles_by_title(arr_description)
    articles_by_description = get_articles_by_description(arr_description)
    articles_general = get_articles_general(arr_description)
    # articles = list(OrderedDict.fromkeys(chain(articles_by_title, articles_by_description, articles_general)))
    articles = articles_general | articles_by_title | articles_by_description
    return articles


def get_articles(description=None, items_per_page=None, page=None):

    items_per_page = items_per_page if items_per_page else 6
    page = page if page else 1

    articles = get_feed_articles(description)

    articles = Paginator(articles, items_per_page)
    try:
        articles = articles.page(page)
    except PageNotAnInteger:
        articles = articles.page(1)
    except EmptyPage:
        articles = []

    return articles


def get_feed_main_criteria():
    criteria = Q(
        article__status = Article.STATUS_PUBLISH
    ) | Q(profile_status__status=True)

    return criteria

def get_articles_feed_queryset(description=''):
    if description == '':
        articles = FeedObject.objects.filter(Q(profile_status__status=True) | Q(article__status=Article.STATUS_PUBLISH)).prefetch_related(
                 "content_object",
                 "content_object__author",
                 "content_type",
                 "communities",
                 "communities__taxonomy").order_by("-date", "id").distinct("id", "date","article__publishin")
    else:

        main_criteria = get_feed_main_criteria()
        query = SearchQuery(description)

        articles = FeedObject.objects.annotate(
            rank=SearchRank(Article.VECTOR + ProfileStatus.VECTOR, query)
        ).filter(main_criteria & (Q(profile_status__search_vector=query) | Q(article__search_vector=query))).prefetch_related(
                 "content_object",
                 "content_object__author",
                 "content_type",
                 "communities",
                 "communities__taxonomy").order_by('-rank', "id")

    return articles

def get_articles_general_feed_queryset(description=''):
    if description == '':
        articles = FeedObject.objects.prefetch_related(
                 "content_object",
                 "content_object__author",
                 "content_type",
                 "communities",
                 "communities__taxonomy").order_by("-article__publishin")
    else:

        query = SearchQuery(description)

        articles = FeedObject.objects.annotate(
            rank=SearchRank(Article.VECTOR, query)
        ).filter(Q(article__search_vector=query)).prefetch_related(
                 "content_object",
                 "content_object__author",
                 "content_type",
                 "communities",
                 "communities__taxonomy").order_by('-rank')

    return articles

def get_question_feed_queryset(description=''):
    if description == '':
        questions = FeedObject.objects.filter(question__id__isnull=False).prefetch_related(
                 "content_object",
                 "content_object__author",
                 "content_type",
                 "communities",
                 "communities__taxonomy").order_by("-question__question_date")
    else:
        query = SearchQuery(description)

        questions = FeedObject.objects.annotate(
            rank=SearchRank(Question.VECTOR, query)
        ).filter(question__search_vector=query).prefetch_related(
                 "content_object",
                 "content_object__author",
                 "content_type",
                 "communities",
                 "communities__taxonomy").order_by('-rank')

    return questions

def get_articles_feed(description='', items_per_page=6, page=1):

    items_per_page = items_per_page if items_per_page else 6
    page = page if page else 1

    articles = get_articles_feed_queryset(description)

    articles = Paginator(articles, items_per_page)

    try:
        articles = articles.page(page)
    except PageNotAnInteger:
        articles = articles.page(1)
    except EmptyPage:
        articles = []

    return articles

def get_feed_questions(description='', items_per_page=None, page=None):

    items_per_page = items_per_page if items_per_page else 6
    page = page if page else 1

    questions = get_question_feed_queryset(description)

    questions = Paginator(questions, items_per_page)
    try:
        questions = questions.page(page)
    except PageNotAnInteger:
        questions = questions.page(1)
    except EmptyPage:
        questions = []

    return questions