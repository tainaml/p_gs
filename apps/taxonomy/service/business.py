import logging

from django.db.models import Q

from ..models import Taxonomy

__author__ = 'phillip'

logger = logging.getLogger('general')


def __get_related_list__(taxonomy=None, taxonomy_list=None):
    if not taxonomy_list:
        taxonomy_list = []

    taxonomy_list.append(taxonomy)

    if taxonomy.parent and taxonomy.parent not in taxonomy_list:
        return __get_related_list__(taxonomy.parent, taxonomy_list)

    return list(reversed(taxonomy_list))

def get_related_taxonomy(taxonomy_list=None):
    """
    This method return the all parent tree of a taxonomy's list

    :rtype : object
    :param taxonomy_list:
    :return:
    """
    if not taxonomy_list:
        taxonomy_list = []

    taxonomies = []
    for taxonomy in taxonomy_list:
        list = __get_related_list__(taxonomy)

        for child_taxonomy in list:
            if child_taxonomy not in taxonomies:
                taxonomies.append(child_taxonomy)

    return taxonomies


def __get_related_list_top_down__(taxonomy=None, taxonomy_list=None):

    if not taxonomy_list:
        taxonomy_list = []

    if not taxonomy:
        return taxonomy_list

    taxonomy_list.append(taxonomy)

    try:
        if taxonomy.taxonomies_children.all():
            children_taxonomies = taxonomy.taxonomies_children.all()

            for child_taxonomy in children_taxonomies:

                __get_related_list_top_down__(child_taxonomy, taxonomy_list)
    except Exception, e:
        logger.error(e.message)

    return taxonomy_list

def get_related_list_top_down(taxonomy_list=None):

    if not taxonomy_list:
        taxonomy_list = []

    taxonomies = []

    for taxonomy in taxonomy_list:
        t_list = __get_related_list_top_down__(taxonomy)

        for child_taxonomy in t_list:
            if child_taxonomy not in taxonomies:
                taxonomies.append(child_taxonomy)

    return taxonomies


def save_taxonomies_for_model(model=None, taxonomi_list=None):

    taxonomy_to_associate = get_related_taxonomy(taxonomi_list)

    model.taxonomies = taxonomy_to_associate
    model.save()

    return True

def get_taxonomies_by_model(model=None):
    return model.taxonomies

def get_categories(list_ids=None):

    if list_ids and isinstance(list_ids, list):
        criteria = Q(term__description__icontains="categoria") & Q(id__in=list_ids)
    else:
        criteria = Q(term__description__icontains="categoria")

    try:
        categories = Taxonomy.objects.filter(criteria)
    except Taxonomy.DoesNotExist:
        categories = Taxonomy.objects.none()

    return categories

def get_category_from_slug(slug):

    criteria = Q(term__description__icontains="categoria") & Q(slug=slug)

    try:
        categories = Taxonomy.objects.filter(criteria)
    except Taxonomy.DoesNotExist:
        categories = Taxonomy.objects.none()

    return categories