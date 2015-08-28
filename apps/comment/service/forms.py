from django.contrib.auth.models import User
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
        return Business.create_comment(self.user, self.cleaned_data)

    def is_valid(self):

        valid = super(CreateCommentForm, self).is_valid()

        if not self.user or not self.user.is_authenticated:
            self.add_error(None,
                           ValidationError(('User must be authenticated.'),
                                           code='is_not_authenticated'))
            valid = False

        try:
            entity_to_comment = settings.ENTITY_TO_COMMENT
        except AttributeError:
            entity_to_comment = False

        if not entity_to_comment or self.cleaned_data[
            'content_type'] not in entity_to_comment:
            self.add_error(None,
                           ValidationError(('Content Type is not specified.'),
                                           code='content_is_not_specified'))
            valid = False

        return valid

class EditCommentForm(IdeiaForm):

    content = forms.CharField(max_length=512, required=True)

    def __init__(self, user=None, instance=None, *args, **kargs):
        self.user = user
        self.instance = instance

        super(EditCommentForm, self).__init__(*args, **kargs)


    def is_valid(self):

        valid = super(EditCommentForm, self).is_valid()

        if not self.user or not self.user.is_authenticated:
            self.add_error(None,
                           ValidationError(('User must be authenticated.'),
                                           code='is_not_authenticated'))
            valid = False

        if self.user and self.instance.author and self.instance.author != self.user:
            self.add_error(None,
                           ValidationError(('comment edit permission denied!'),
                                           code='is_not_authenticated'))
            valid = False


        return valid

    def __process__(self):
        return Business.edit_comment(self.instance, self.cleaned_data)