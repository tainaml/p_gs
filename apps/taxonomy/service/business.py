import copy

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



