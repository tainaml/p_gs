from django.core.exceptions import ValidationError
from django.conf import settings

from apps.community.models import Community
from apps.custom_base.service.custom import forms, IdeiaForm
import business as Business

entity_to_complaint = settings.ENTITY_TO_COMPLAINT if hasattr(settings, 'ENTITY_TO_COMPLAINT') else False


class ComplaintForm(IdeiaForm):
    description = forms.CharField(max_length=512, required=False)
    complaint_type = forms.ModelChoiceField(queryset=Business.get_type_complaint(), required=True)
    content_type = forms.CharField(max_length=20, required=True)
    object_id = forms.IntegerField(required=True)
    community_complaint = forms.ModelMultipleChoiceField(queryset=Community.objects.all(), required=False)

    def __init__(self, user=None, *args, **kwargs):
        super(ComplaintForm, self).__init__(*args, **kwargs)
        self.user = user

    def is_valid(self):

        valid = super(ComplaintForm, self).is_valid()

        try:
            entity_to_complaint = settings.ENTITY_TO_COMPLAINT
        except AttributeError:
            entity_to_complaint = False

        if not entity_to_complaint or self.cleaned_data['content_type'] not in entity_to_complaint:
            self.add_error(None,
                           ValidationError(('Content Type is not specified.'),
                                           code='content_is_not_specified'))
            valid = False

        return valid

    def __process__(self):
        return Business.create_complaint(parameters=self.cleaned_data, user=self.user)