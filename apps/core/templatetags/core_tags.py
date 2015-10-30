from distutils.command.register import register

from django import template
from django.contrib.contenttypes.models import ContentType
from django.db.models import Q
from django.http import Http404
from apps.taxonomy.service import business as TaxonomiesBusiness
from django.utils import timezone

from apps.article.models import Article
from apps.feed.models import FeedObject


register = template.Library()


@register.inclusion_tag('core/templatetags/relevance-box.html', takes_context=True)
def relevance_box(context, content_object, count=4, template_path='core/partials/relevance/article-base.html'):

    try:
        record_type = ContentType.objects.get(model="article")

        records = FeedObject.objects.filter(
            taxonomies=content_object.taxonomy,
            content_type=record_type,
            article__status=Article.STATUS_PUBLISH,
            article__publishin__lte=timezone.now()
        ).order_by(
            '-relevance',
            '-article__publishin'
        ).distinct(
            'relevance',
            'article__publishin',
            'object_id',
            'content_type_id'
        )[:count]

    except ValueError:
        raise Http404()

    return {
        'records': records,
        'request': context['request'],
        'template_path': template_path
    }


@register.inclusion_tag('core/templatetags/last_questions.html', takes_context=True)
def last_questions(context, content_object, content_type, count=4, template_path=None):
    try:
        record_type = ContentType.objects.get(model="question")

        records = FeedObject.objects.filter(
            taxonomies=content_object.taxonomy,
            content_type=record_type,
            question__question_date__lte=timezone.now()
        ).order_by(
            '-relevance',
            '-question__question_date'
        ).distinct(
            'relevance',
            'question__question_date',
            'object_id',
            'content_type_id'
        )[:count]

    except ValueError:
        raise Http404()

    return {
        'questions': records
    }


@register.inclusion_tag("core/templatetags/related-posts-box.html", takes_context=True)
def related_posts_box(context, instance, post_type=None, count=4, template_path=None):

    try:
        content_type = ContentType.objects.get_for_model(instance)

        post_type = ContentType.objects.get(model=post_type) if post_type else content_type

        if template_path is None:
            template_path = 'core/partials/related-posts/%s-base.html' % post_type.model

        feed_obj = FeedObject.objects.get(content_type=content_type, object_id=instance.id)

        feed_records = FeedObject.objects.filter(
            Q(taxonomies__in=feed_obj.taxonomies.all()) &
            Q(taxonomies__term__description__icontains="comunidade") &
            Q(content_type=post_type) &
            (
                (
                    Q(article__status=Article.STATUS_PUBLISH) &
                    Q(article__publishin__lte=timezone.now())
                ) | Q(question__title__isnull=False)
            )
        ).exclude(
            Q(object_id=instance.id)
        ).order_by(
            "-date"
        ).distinct(
            "date",
            "object_id",
            "content_type_id"
        )[:count]

    except ValueError:
        raise Http404()

    return {
        'feed_records': feed_records,
        'request': context['request'],
        'template_path': template_path
    }











