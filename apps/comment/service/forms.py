from django.core.exceptions import ValidationError
from django.conf import settings
from django.core.serializers.json import DjangoJSONEncoder
from django.utils.encoding import force_text
from django.utils.functional import Promise
from apps.comment.models import Comment
from django.utils.translation import ugettext as _

from apps.custom_base.service.custom import forms, IdeiaForm
import business as Business


class LazyEncoder(DjangoJSONEncoder):

    def default(self, obj):
        if isinstance(obj, Promise):
            return force_text(obj)
        return super(LazyEncoder, self).default(obj)


json_encode = LazyEncoder().encode


class CreateCommentForm(IdeiaForm):
    content = forms.CharField(
        max_length=settings.COMMENT_TEXT_LIMIT if hasattr(settings, "COMMENT_TEXT_LIMIT") else 10000,
        required=True,
    )
    content_type = forms.CharField(max_length=20, required=True)
    content_object_id = forms.IntegerField(required=True)

    def __init__(self, user=None, *args, **kwargs):
        self.user = user
        super(CreateCommentForm, self).__init__(*args, **kwargs)

    def __process__(self):
        return Business.create_comment(self.user, self.cleaned_data)

    def clean(self):
        self.cleaned_data = super(CreateCommentForm, self).clean()
        if 'content' in self.cleaned_data:
            self.cleaned_data['content'] = self.cleaned_data['content'].strip()

        return self.cleaned_data

    def is_valid(self):

        valid = super(CreateCommentForm, self).is_valid()

        if not self.user or not self.user.is_authenticated:
            self.add_error(None,
                           ValidationError(('User must be authenticated.'),
                                           code='is_not_authenticated'))
            valid = False

        if 'content' in self.cleaned_data and self.cleaned_data['content'] == '':
            self.add_error('content',
                           ValidationError(('Is not possible to comment only with white spaces.'),
                                           code='white_spaces'))
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

    content = forms.CharField(
        max_length=settings.COMMENT_TEXT_LIMIT if hasattr(settings, "COMMENT_TEXT_LIMIT") else 10000,
        required=True,
    )
    comment_id = forms.IntegerField(required=True)

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

        if not self.instance:
            self.add_error(None,
                           ValidationError(('Comment doesn\'t exist.'),
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


class ListCommentForm(IdeiaForm):

    content_id = forms.IntegerField(min_value=1, required=True)
    content_type = forms.CharField(required=True)
    page = forms.IntegerField(min_value=1, required=False)

    def __init__(self, itens_per_page=10, *args, **kwargs):
        self.itens_per_page = itens_per_page
        super(ListCommentForm, self).__init__(*args, **kwargs)

    def clean(self):
        cleaned_data = super(ListCommentForm, self).clean()
        cleaned_data['page'] = cleaned_data['page']\
            if 'page' in cleaned_data and cleaned_data['page'] else 1

        return cleaned_data

    def is_valid(self):
        valid = super(ListCommentForm, self).is_valid()

        if 'content_type' in self.cleaned_data and self.cleaned_data['content_type'] not in settings.ENTITY_TO_COMMENT:
            self.add_error(None,
                           ValidationError(('ContentType not found in comment contentType list.'),
                                           code='comment_content_type_not_found'))

        return valid

    def __process__(self):

        return Business.get_comments_by_content_type_and_id(
            self.cleaned_data['content_type'],
            self.cleaned_data['content_id'],
            self.itens_per_page,
            self.cleaned_data['page']
        )


class CommentDeleteForm(IdeiaForm):

    comment = forms.ModelChoiceField(queryset=Comment.objects.all())
    author = None

    def __init__(self, author=None, *args, **kwargs):
        self.author=author

        super(CommentDeleteForm, self).__init__(*args, **kwargs)

    def is_valid(self):
        is_valid = super(CommentDeleteForm, self).is_valid()

        if 'comment' in self.cleaned_data and self.cleaned_data.get('comment').author != self.author:
            is_valid = False
            self.add_error('__all__', ValidationError(_('You do not have permission to perform this action.'),
                                                      code='without-permission'))

        return is_valid

    def __process__(self):
        return Business.delete_comment(self.cleaned_data.get('comment'))
