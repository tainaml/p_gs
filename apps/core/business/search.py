from django.contrib.auth.models import User
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from django.db.models import Q

from apps.article.models import Article
from apps.community.models import Community
from apps.question.models import Question


def get_communities(description=None, items_per_page=None, page=None, startswith=False):

    items_per_page = items_per_page if items_per_page else 6
    page = page if page else 1

    if startswith:
        criteria = Q(title__unaccent__istartswith=description)
    else:
        criteria = Q(title__unaccent__icontains=description)

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
        criteria = (Q(first_name__unaccent__icontains=description) | Q(last_name__unaccent__icontains=description))

    users = User.objects.filter(Q(is_active=True) & criteria).distinct('id')

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

    articles = Article.objects.filter(
        Q(status=Article.STATUS_PUBLISH) &
        (
            Q(title__unaccent__icontains=description) |
            Q(text__unaccent__icontains=description)
        )
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

    questions = Question.objects.filter(
        Q(title__unaccent__icontains=description) |
        Q(description__unaccent__icontains=description)
    ).order_by('-question_date').distinct('id', 'question_date')

    questions = Paginator(questions, items_per_page)
    try:
        questions = questions.page(page)
    except PageNotAnInteger:
        questions = questions.page(1)
    except EmptyPage:
        questions = []

    return questions
