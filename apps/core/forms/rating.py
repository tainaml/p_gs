from django.forms import HiddenInput
from apps.core.models.rating import Rating
from apps.custom_base.service.custom import IdeiaModelForm

class RatingWidget(HiddenInput):

    def render(self, name, value, attrs=None):

        final_attrs = {'data-toggle': 'rating-value'}
        if attrs:
            final_attrs.update(attrs)
        return super(RatingWidget, self).render(name=name, value=value, attrs=final_attrs)



class FormRating(IdeiaModelForm):

    class Meta:
        model = Rating
        exclude = ['rating_date']
        widgets = {
            'content_type': HiddenInput(),
            'object_id': HiddenInput(),
            'value': RatingWidget()
        }
