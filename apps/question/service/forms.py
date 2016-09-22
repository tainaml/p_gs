from django.core.exceptions import ValidationError
from django.db import transaction
from django.utils.text import slugify
from django.utils.translation import ugettext as _
from django.conf import settings
from ideia_summernote.widget import SummernoteWidget
from apps.question.models import Answer
from apps.custom_base.service.custom import forms, IdeiaForm, IdeiaModelForm

import business as Business
import re


class CreateQuestionForm(IdeiaModelForm):

    title = forms.CharField(max_length=settings.QUESTION_TITLE_LIMIT if hasattr(settings, "QUESTION_TITLE_LIMIT") else 100, required=True)
    slug = forms.SlugField(max_length=300, required=False)
    description = forms.CharField(max_length=settings.QUESTION_TEXT_LIMIT if hasattr(settings, "QUESTION_TEXT_LIMIT") else 10000, widget=SummernoteWidget(editor_conf='question'), required=True)

    user = None

    class Meta:
        model = Business.Question
        exclude = ['author', 'question_date', 'search_vector']

    def is_valid(self):
        valid = super(CreateQuestionForm, self).is_valid()
        return valid

    def __init__(self, data=None, files=None, user=None, *args, **kargs):
        super(CreateQuestionForm, self).__init__(data, files, *args, **kargs)
        self.set_author(user)

    def set_author(self, user):
        self.user = user

    def clean_description(self):
        regex = re.compile(r'<p>&nbsp;</p>')
        _description = regex.sub('', self.cleaned_data.get('description'))

        return _description

    def clean_slug(self):
        _slug = self.cleaned_data.get('slug', None)
        _title = self.cleaned_data.get('title')
        _slug = _slug if _slug is not None else slugify(_title)
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
    description = forms.CharField(widget=SummernoteWidget(editor_conf='reply'), max_length=settings.ANSWER_TEXT_LIMIT if hasattr(settings, "ANSWER_TEXT_LIMIT") else 10000, required=True)

    def __init__(self, instance=None, user=None, *args, **kargs):
        super(CommentReplyForm, self).__init__(instance, *args, **kargs)
        self.instance = instance
        self.user = user
        self.question = instance["question_id"]
        self.description = instance["description"]

    def is_valid(self):
        is_valid = super(CommentReplyForm, self).is_valid()

        description = self.cleaned_data.get('description', '').strip()

        if description == '' or description is None:
            self.add_error('description', ValidationError(_('Your answer can not be blank'), code='description'))
            is_valid = False

        return is_valid

    def clean_description(self):
        description = self.cleaned_data.get('description', '').strip()
        return description

    def __process__(self):
        return Business.comment_reply(self.cleaned_data, self.user, self.question)


class ListAnswerForm(IdeiaForm):

    question_id = forms.IntegerField(min_value=1, required=True)
    page = forms.IntegerField(min_value=1, required=False)

    def __init__(self, question=None, itens_by_page=10, *args, **kwargs):
        self.question = question
        self.itens_by_page = itens_by_page
        super(ListAnswerForm, self).__init__(*args, **kwargs)

    def clean(self):
        cleaned_data = super(ListAnswerForm, self).clean()
        cleaned_data['page'] = cleaned_data['page']\
            if 'page' in cleaned_data and cleaned_data['page'] else 1

        return cleaned_data

    def __process__(self):

        return Business.get_answers_by_question(
            question=self.question,
            items_per_page=self.itens_by_page,
            page=self.cleaned_data['page']
        )


class EditAnswerForm(IdeiaForm):
    description = forms.CharField(widget=SummernoteWidget(editor_conf='reply'), max_length=settings.ANSWER_TEXT_LIMIT if hasattr(settings, "ANSWER_TEXT_LIMIT") else 10000, required=True)

    user = None

    def __init__(self, instance=None, user=None, *args, **kwargs):
        self.instance = instance
        self.user = user
        super(EditAnswerForm, self).__init__(*args, **kwargs)

    def set_author(self, user):
        self.user = user

    def is_valid(self):
        is_valid = super(EditAnswerForm, self).is_valid()

        if not self.user or not self.user.is_authenticated():
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


class RemoveAnswerForm(IdeiaForm):

    answer = forms.ModelChoiceField(queryset=Answer.objects.all(), required=True)

    def __init__(self, *args, **kwargs):
        super(RemoveAnswerForm, self).__init__(*args, **kwargs)

    def is_valid(self):
        is_valid = super(RemoveAnswerForm, self).is_valid()
        return is_valid

    def __process__(self):
        return Business.remove_answer(self.cleaned_data.get('answer'))
