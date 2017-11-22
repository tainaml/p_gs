from apps.community.models import Community
from apps.core.models.course import Course
from apps.feed.models import ProfileStatus
from apps.question.models import Question
from django import template
from django.contrib.auth import get_user_model

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
def communities_slider():

    communities = Community.objects.all().order_by("?")

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


def article_section(slug, feed_articles, quantity, class_name):
    segmented_feed_article = feed_articles[slug]
    feed_list = []
    segmented_feed_article = list(segmented_feed_article)
    for index in range(0, quantity):
        feed_list.append(segmented_feed_article.pop())


    return {"feed_list": feed_list, "class_name": class_name}



@register.inclusion_tag('home/blocks/article/large.html')
def article_section_large(slug, feed_articles, quantity, class_name):
    return article_section(slug, feed_articles, quantity, class_name)\

@register.inclusion_tag('home/blocks/article/half3.html')
def article_section_half(slug, feed_articles, quantity, class_name):
    community = None
    try:
        Community.objects.get(taxonomy__slug=slug)
    except Community.DoesNotExist:
        pass

    response =  article_section(slug, feed_articles, quantity, class_name)
    response.update({"community": community})
    print response

    return response

