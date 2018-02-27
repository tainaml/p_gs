from apps.article.models import Article
from apps.community.models import Community
from apps.core.models.course import Course
from apps.feed.models import ProfileStatus, FeedObject
from apps.question.models import Question
from django import template
from django.contrib.auth import get_user_model
from django.db.models import Q
from django.core.cache import cache

register = template.Library()


@register.inclusion_tag('userprofile/partials/join-us.html', takes_context=True)
def join_us(context, quantity):
    request = context['request']
    User = get_user_model()
    users = User.objects.filter(profile__profile_picture__isnull=False).prefetch_related("profile").order_by("?")[:quantity]
    count = User.objects.all().count()
    # Workaround
    count =  int(count / 1000) * 1000

    return {"users": users, "count": count, "request": request}


@register.inclusion_tag('home/partials/communities-slider.html')
def communities_slider(category=None, cache_time=3600):

    communities_queryset = Community.objects.all().order_by("?")

    if category is None:
        cache_key = "all"
        communities = cache.get(cache_key)
        if communities is None:
            communities = communities_queryset
            cache.set(cache_key, list(communities), cache_time)

    else:
        cache_key = "communities_{0}".format(category.slug)
        communities = cache.get(cache_key)
        if communities is None:
            communities = communities_queryset.filter(Q(taxonomy=category) | Q(taxonomy__parent=category))
            for community in communities:
                #workaround to execute the query
                community.followers = community.followers
            cache.set(cache_key, communities, cache_time)





    return {"communities": communities}


@register.inclusion_tag('home/partials/commits.html')
def commits(quantity):

    commits = ProfileStatus.objects.all().prefetch_related("author").order_by("-publishin")[:quantity]

    return {"commits": commits}


@register.inclusion_tag('home/partials/last-courses.html')
def last_courses(quantity):

    last_courses = Course.objects.all().order_by("-createdin")[:quantity]

    return {"last_courses": last_courses}

@register.inclusion_tag('home/partials/last-questions.html')
def last_questions(quantity):

    questions = Question.objects.all().order_by("-question_date")[:quantity]

    return {"questions": questions}\


def article_section(request, slug, feed_articles, quantity, class_name):

    feed_list = []
    for index in range(0, quantity):
         feed_list.append(feed_articles[slug]["items"].pop())


    return {"request": request, "feed_list": feed_list, "class_name": class_name, "community": feed_articles[slug]["community"]}



@register.inclusion_tag('home/blocks/article/large.html', takes_context=True)
def article_section_large(context, slug, feed_articles, quantity, class_name):
    request = context['request']
    return article_section(request, slug, feed_articles, quantity, class_name)\

@register.inclusion_tag('home/blocks/article/half3.html', takes_context=True)
def article_section_half(context, slug, feed_articles, quantity, class_name):
    request = context['request']
    response =  article_section(request, slug, feed_articles, quantity, class_name)
    return response

@register.inclusion_tag('home/partials/videos.html')
def video_section(quantity):
    videos  = Article.objects.filter(
            status=Article.STATUS_PUBLISH,
            feed__tags__tag_slug='video'
        ).prefetch_related(
            'feed', 'author'
        ).order_by('-publishin')[:quantity]

    return {
        "videos": videos
    }

@register.inclusion_tag('home/blocks/article/large.html')
def news(feed_articles, quantity):

    ids = []
    for item in feed_articles:
        feeds = feed_articles[item]

        for feed in feeds["items"]:
            ids.append(feed.id)
    feed_list = FeedObject.objects.prefetch_related(
        "content_object",
        "content_type",
        "content_object__author",
        "content_object__author__profile",
        "communities",
        "communities__taxonomy").filter(
                Q(article__status=Article.STATUS_PUBLISH)
                & Q(object_id__isnull=False)
                & Q(tags__tag_slug='noticia')
                & Q(official=True)).exclude(id__in=ids).order_by("-article__publishin")[:quantity]



    return {"feed_list": feed_list}



