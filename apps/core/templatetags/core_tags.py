from distutils.command.register import register

from django import template
from django.contrib.contenttypes.models import ContentType
from django.http import Http404
from apps.taxonomy.service import business as TaxonomiesBusiness


from apps.taxonomy.models import ObjectTaxonomy


register = template.Library()


@register.inclusion_tag('core/templatetags/relevance-box.html', takes_context=True)
def relevance_box(context, taxonomy, content_type, count=5, template_path=None):

    try:
        # content_type = ContentType.objects.get(model=content_type)

        records = ObjectTaxonomy.objects.filter(content_type=content_type).order_by('relevance')[:count]

    except ValueError:
        raise Http404()

    return {
        'request': context['request']
    }


@register.inclusion_tag('core/templatetags/last_questions.html', takes_context=True)
def last_questions(context, content_object, content_type, count=4, template_path=None):

    try:
        taxonomies = TaxonomiesBusiness.get_taxonomies_by_model(content_object)
        tax_ids = []
        for tax in taxonomies:
            tax_ids.append(tax.taxonomy.id)

        record_type = ContentType.objects.get(model='question')

        records = ObjectTaxonomy.objects.filter(taxonomy__in=tax_ids, content_type=record_type).prefetch_related('content_object').distinct('object_id')[:count]

    except ValueError:
        raise Http404()

    return {
        'questions': records
    }