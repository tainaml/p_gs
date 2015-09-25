from distutils.command.register import register

from django import template
from django.contrib.contenttypes.models import ContentType
from django.http import Http404

from apps.taxonomy.service import business as TaxonomyBusiness
from apps.taxonomy.models import ObjectTaxonomy


register = template.Library()


@register.inclusion_tag('core/templatetags/relevance-box.html', takes_context=True)
def relevance_box(context, content_object, content_type="article", count=4, template_path='core/partials/relevance/article-base.html'):

    try:
        feed_type = ContentType.objects.get(model="feedobject")
        record_type = ContentType.objects.get(model=content_type)

        taxonomies = TaxonomyBusiness.get_taxonomies_by_model(content_object)
        taxonomies_list = [tax.taxonomy.id for tax in taxonomies]

        records = ObjectTaxonomy.objects.filter(
            taxonomy__in=taxonomies_list,
            content_type=feed_type,
            feed_obj__content_type=record_type
        ).order_by(
            '-feed_obj__relevance',
        ).distinct(
            'feed_obj__relevance',
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