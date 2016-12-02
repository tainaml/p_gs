__author__ = 'phillip'
from apps.core.models.rating import Rating

def rate(params=None):
    if not params:
        params = {}

    rating = Rating(

    )
    rating.save()