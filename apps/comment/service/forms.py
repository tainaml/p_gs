from django.core.exceptions import ValidationError
from custom_forms.custom import forms, IdeiaForm
import business as Business
from django.conf import settings

class CreateCommentForm(IdeiaForm):

    content = forms.CharField(max_length=512, required=True)
    content_type = forms.CharField(max_length=20, required=True)
    content_object_id = forms.IntegerField(required=True)

    def __init__(self, user=None, *args, **kargs):
        self.user = user
        super(CreateCommentForm, self).__init__(*args, **kargs)


    def __process__(self):
        Business.create_comment(self.user, self.cleaned_data)

    def is_valid(self):

        valid = super(CreateCommentForm, self).is_valid()


        if not self.user or not self.user.is_authenticated:
            self.add_error('content', ValidationError(('User must be authenticated.'), code='is_not_authenticated'))
            valid = False

        if not settings.ENTITY_TO_COMMENT or self.cleaned_data['content_type'] not in settings.ENTITY_TO_COMMENT:
            self.add_error(None, ValidationError(('Content Type is not specified.'), code='content_is_not_specified'))
            valid = False

        return valid