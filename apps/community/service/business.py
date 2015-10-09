from ..models import Community


def get_community_by_params(params={}, order_by=[], limit=None, offset=None):
    try:
        community = Community.objects.filter(**params).order_by(*order_by)[offset:limit]
        print "-- community --"
        print community
    except Community.DoesNotExist:
        return False

    return community

def get_communities(taxonomies_id=None):
    try:
        communities = Community.objects.filter(taxonomy__in=taxonomies_id)
    except Community.DoesNotExist:
        return None

    return communities

def get_community(slug=None):
    try:
        community = Community.objects.get(slug=slug)
    except Community.DoesNotExist:
        return None

    return community