from ..models import Community


def get_community_by_params(params={}, order_by=[], limit=None, offset=None):
    try:
        community = Community.objects.filter(**params).order_by(*order_by)[offset:limit]
    except Community.DoesNotExist:
        return False

    return community


def get_community(slug=None):
    try:
        community = Community.objects.get(slug=slug)
    except Community.DoesNotExist:
        return None

    return community