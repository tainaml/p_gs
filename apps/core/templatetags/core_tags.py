from distutils.command.register import register

from django import template
from django.contrib.contenttypes.models import ContentType
from django.db.models import Count
from django.http import Http404

from apps.taxonomy.service import business as TaxonomyBusiness
from apps.taxonomy.models import ObjectTaxonomy


register = template.Library()


@register.inclusion_tag('core/templatetags/relevance-box.html', takes_context=True)
def relevance_box(context, content_object, content_type, count=5, template_path='core/partials/relevance/article-base.html'):

    try:
        records_type = ContentType.objects.get(model=content_type)

        taxonomies = TaxonomyBusiness.get_taxonomies_by_model(content_object)
        taxonomies_list = [tax.taxonomy.id for tax in taxonomies]

        records = ObjectTaxonomy.objects.filter(taxonomy__in=taxonomies_list, content_type=records_type)\
                      .order_by('-articles__relevance',
                                '-articles__publishin')\
                      .distinct('articles__relevance', 'articles__publishin', 'object_id', 'content_type_id')[:count]

    except ValueError:
        raise Http404()

    return {
        'records': records,
        'request': context['request'],
        'template_path': template_path
    }