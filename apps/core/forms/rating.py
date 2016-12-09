from apps.core.models.rating import Rating

__author__ = 'phillip'
from apps.custom_base.service.custom import IdeiaModelForm

class FormRating(IdeiaModelForm):

    class Meta:
        model = Rating
        exclude = ['rating_date']
