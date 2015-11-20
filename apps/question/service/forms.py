from ckeditor.widgets import CKEditorWidget
from django.core.exceptions import ValidationError
from django.db import models
from django.db import transaction
from django.utils.text import slugify
from custom_forms.custom import forms, IdeiaForm, IdeiaModelForm
import business as Business
from django.conf import settings


class CreateQuestionForm(IdeiaModelForm):

    title = forms.CharField(max_length=256, required=True)
    slug = forms.SlugField(max_length=300, required=False)
    description = forms.CharField(max_length=2048, required=True, widget=CKEditorWidget(config_name='question'))

    user = None

    class Meta:
        model = Business.Question
        exclude = ['author', 'question_date']

    def is_valid(self):
        valid = super(CreateQuestionForm, self).is_valid()
        return valid

    def __init__(self, data=None, files=None, user=None, *args, **kargs):
        super(CreateQuestionForm, self).__init__(data, files, *args, **kargs)
        self.set_author(user)

    def set_author(self, user):
        self.user = user

    def clean_slug(self):
        _slug = self.cleaned_data.get('slug', '')
        _title = self.cleaned_data.get('title')
        _slug = _slug if _slug else slugify(_title)
        return _slug

    @transaction.atomic()
    def __process__(self):
        self.instance = Business.save_question(self.user, self.cleaned_data)
        return self.instance


class EditQuestionForm(CreateQuestionForm):

    def set_author(self, user):
        self.user = user

    def is_valid(self):
        is_valid = super(EditQuestionForm, self).is_valid()

        if not self.user or not self.user.is_authenticated:
            self.add_error(None,
                           ValidationError(('User must be authenticated.'),
                                           code='is_not_authenticated'))
            is_valid = False

        if self.user != self.instance.author:
            self.add_error(None,
            ValidationError(('User dont have access'),
                                               code='is_not_permission'))
            is_valid = False

        return is_valid

    def __process__(self):
        question = Business.update_question(self.cleaned_data, self.instance)
        return question


class CommentReplyForm(IdeiaForm):
    description = forms.CharField(max_length=2048, required=True, widget=CKEditorWidget(config_name='question'))

    def __init__(self, instance=None, user=None, *args, **kargs):
        super(CommentReplyForm, self).__init__(instance, *args, **kargs)
        self.instance = instance
        self.user = user
        self.question = instance["question_id"]
        self.description = instance["description"]

    def __process__(self):
        return Business.comment_reply(self.cleaned_data, self.user, self.question)


class EditAnswerForm(IdeiaModelForm):
    description = forms.CharField(max_length=2048, required=True, widget=CKEditorWidget(config_name='question'))

    user = None

    class Meta:
        model = Business.Answer
        exclude = ['author', 'answer_date', 'question']

    def set_author(self, user):
        self.user = user

    def is_valid(self):
        is_valid = super(EditAnswerForm, self).is_valid()

        if not self.user or not self.user.is_authenticated:
            self.add_error(None,
                           ValidationError(('User must be authenticated.'),
                                           code='is_not_authenticated'))
            is_valid = False

        if self.user != self.instance.author:
            self.add_error(None,
            ValidationError(('User dont have access'),
                                               code='is_not_permission'))
            is_valid = False

        return is_valid

    def __process__(self):
        return Business.update_reply(self.cleaned_data, self.instance)