from distutils.command.register import register

from django import template
from django.contrib.contenttypes.models import ContentType
from django.http import Http404

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