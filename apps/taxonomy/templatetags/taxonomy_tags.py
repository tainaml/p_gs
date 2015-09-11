from django import template
from ..service import business as Business

register = template.Library()

@register.inclusion_tag('taxonomy/taxonomies.html')
def taxonomies(content_object):

    taxonomies = Business.get_taxonomies_by_model(content_object)


    return {
        'taxonomies': taxonomies
    }
