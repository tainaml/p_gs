from distutils.command.register import register

from django import template
from django.contrib.contenttypes.models import ContentType
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
    pass