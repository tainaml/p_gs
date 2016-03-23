from django.contrib.contenttypes.models import ContentType
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from django.db.models import Q

from apps.feed.models import FeedObject
from apps.taxonomy.service import business as BusinessTaxonomy
from apps.feed.service import business as BusinessFeed


def save_taxonomies(instance=None, data=None):
    taxonomies = BusinessTaxonomy.save_taxonomies_for_model(instance, data['taxonomies'])
    return taxonomies


def save_feed_item(instance, data=None):
    feed_object = BusinessFeed.feed_get_or_create(instance)
    feed_object.date = instance.question_date
    feed_object.save()
    return feed_object


def get_related(question_id, record_type=None, items_per_page=None, page=None):

    content_type = ContentType.objects.get(model="question")
    record_type = ContentType.objects.get(model=record_type)

    try:

        feed_question = FeedObject.objects.get(
            Q(object_id=question_id) &
            Q(content_type=content_type)
        )

        related_questions = FeedObject.objects.filter(
            Q(taxonomies__in=feed_question.taxonomies.all()) &
            Q(content_type=record_type)
        ).exclude(
            Q(object_id=question_id) &
            Q(content_type=content_type)
        ).order_by(
            '-date'
        )

    except Exception, e:
        return False

    if items_per_page and page:
        related_questions = Paginator(related_questions, items_per_page)
        try:
            related_questions = related_questions.page(page)
        except PageNotAnInteger:
            related_questions = related_questions.page(1)
        except EmptyPage:
            related_questions = []

    return related_questions
