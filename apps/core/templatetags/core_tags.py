# coding=utf-8
import re
from apps.core.templatetags.amp_tags import do_amp_normalize_text
from django import template
from django.conf import settings
from django.db.models import Q
from django.http import Http404
from django.template.defaultfilters import stringfilter, truncatechars
from django.template.loader import render_to_string
from django.utils import timezone
from django.core.cache import cache
from django.utils.html import strip_tags
from django.utils.safestring import mark_safe
from django.utils.text import slugify
from django.utils.translation import ugettext as _
from apps.article.models import Article
from apps.community.models import Community
from apps.core.business.content_types import ContentTypeCached
from apps.feed.models import FeedObject
from apps.taxonomy.models import Taxonomy
from apps.temp_comment.models import TempComment
from apps.core.business import feed as FeedBusiness

register = template.Library()


@register.inclusion_tag('core/templatetags/relevance-box.html', takes_context=True)
def relevance_box(context, content_object, count=4, template_path='core/partials/relevance/article-base.html'):
    try:
        record_type = ContentTypeCached.objects.get(model="article")

        records = FeedObject.objects.filter(
            communities__in=[content_object],
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
        ).prefetch_related("content_object")[:count]

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
        record_type = ContentTypeCached.objects.get(model="question")

        records = FeedObject.objects.filter(
            taxonomies=content_object.taxonomy,
            content_type=record_type,
            question__question_date__lte=timezone.now(),
            question__deleted=False
        ).order_by(
            '-relevance',
            '-question__question_date'
        ).distinct(
            'relevance',
            'question__question_date',
            'object_id',
            'content_type_id'
        ).prefetch_related("content_object")[:count]
    except ValueError:
        raise Http404()

    return {
        'questions': records
    }


@register.inclusion_tag("core/templatetags/related-posts-box.html", takes_context=True)
def related_posts_box(context, instance, instance_type, post_type=None, count=4, template_path=None):
    try:
        related_object = FeedBusiness.get_related_posts_from_item(instance_id=instance.id, instance_type=instance_type, count=count)
        if not template_path:
            template_path = related_object.get('template_path')

    except ValueError:
        raise Http404()

    return {
        'feed_records': related_object.get('feed_records'),
        'request': context['request'],
        'template_path': template_path
    }

@register.simple_tag(takes_context=True)
def amp_related_posts_box(context, instance, instance_type, post_type=None, count=4, template_path="core/templatetags/related-posts-box.html"):

    try:
        related_object = FeedBusiness.get_related_posts_from_item(instance_id=instance.id, instance_type=instance_type, count=count)
        if not template_path:
            template_path = related_object.get('template_path')

    except ValueError:
        return ''

    context = {
        'feed_records': related_object.get('feed_records'),
        'template_path': related_object.get('template_path'),
        'is_amp': True
    }

    cleaned = render_to_string(template_path, context=context, request=context.get('request'))
    cleaned = do_amp_normalize_text(cleaned)

    return mark_safe(cleaned)


def __categories_in_cache__(request):

    categories_cached = cache.get("categories")

    if not categories_cached:

        categories_cached = {}
        categories = Taxonomy.objects.filter(term__description="Categoria")
        taxonomies = Taxonomy.objects.filter(parent__in=categories, term__description="Comunidade").order_by("description")

        for taxonomy in taxonomies:
            slug = slugify(taxonomy.parent.description).replace("-", "_")
            if slug not in categories_cached.keys():
                categories_cached[slug] = []
            if hasattr(taxonomy, 'community_related'):
                categories_cached[slug].append(taxonomy.community_related)

        cache.set("categories", categories_cached, None)
    return {
        'categories': categories_cached,
        'request': request
    }

@register.inclusion_tag("core/templatetags/footer.html", takes_context=True)
def footer(context):
    return __categories_in_cache__(context.get('request'))

@register.inclusion_tag("core/templatetags/communities_cached.html", takes_context=True)
def communities_cached(context):
    return __categories_in_cache__(context.get('request'))

@register.simple_tag()
def contact_suggest_community_type():
    return getattr(settings, 'CONTACT_SUGGEST')


@register.simple_tag()
def contact_suggest_community_message():
    return _(u'Olá, gostaria de sugerir a comunidade: ')

@register.inclusion_tag("core/templatetags/old-comments.html", takes_context=True)
def old_comments(context, article):
    comments = TempComment.objects.filter(article=article)

    return {'comments': comments}

@register.inclusion_tag("core/templatetags/old-answers.html", takes_context=True)
def old_answers(context, comment):
    comments = TempComment.objects.filter(parent_google_id=comment.google_id)

    return {'comments': comments}

@register.inclusion_tag("core/templatetags/category-communities-links.html")
def category_communities_links():
    category_communities = Community.objects.filter(taxonomy__term__slug='categoria')

    return {
        'category_communities': category_communities
    }


@register.filter(is_safe=True)
@stringfilter
def seo_description(value):
    string_size = getattr(settings, 'SEO_DESCRIPTION_STRING_SIZE', 160)
    return strip_tags(truncatechars(strip_tags(value), string_size)).strip()