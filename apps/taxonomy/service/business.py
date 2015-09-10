import copy
from django.contrib.contenttypes.models import ContentType
from ..models import ObjectTaxonomy

__author__ = 'phillip'


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


def save_taxonomies_for_model(model=None, taxonomi_list=None):
    content = ContentType.objects.get_for_model(model)
    taxonomy_to_associate = get_related_taxonomy(taxonomi_list)
    ObjectTaxonomy.objects.filter(content_type=content,
                                                     object_id=model.id).delete()

    for taxonomy in taxonomy_to_associate:
        object_taxonomy = ObjectTaxonomy(taxonomy=taxonomy, content_type=content, object_id=model.id)
        object_taxonomy.save()



    return True

def get_taxonomies_by_model(model=None):
    content = ContentType.objects.get_for_model(model)
    return ObjectTaxonomy.objects.filter(content_type=content,
                                                     object_id=model.id).prefetch_related('taxonomy')