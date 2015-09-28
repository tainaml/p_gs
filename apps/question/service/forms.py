from django.core.exceptions import ValidationError
from django.db import models
from django.db import transaction
from custom_forms.custom import forms, IdeiaForm, IdeiaModelForm
import business as Business
from django.conf import settings


class CreateQuestionForm(IdeiaForm):
    title = forms.CharField(max_length=256, required=True)
    description = forms.CharField(max_length=2048, required=True)

    def __init__(self, user=None, *args, **kargs):
        self.user = user
        super(CreateQuestionForm, self).__init__(*args, **kargs)

    @transaction.atomic()
    def __process__(self):
        self.instance = Business.save_question(self.user, self.cleaned_data)
        return self.instance


class EditQuestionForm(IdeiaModelForm):
    title = forms.CharField(max_length=256, required=True)
    description = forms.CharField(max_length=2048, required=True)

    user = None

    class Meta:
        model = Business.Question
        exclude = ['author', 'question_date']

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
        return Business.update_question(self.cleaned_data, self.instance)


class CommentReplyForm(IdeiaForm):
    description = forms.CharField(max_length=2048, required=True)

    def __init__(self, instance=None, user=None, *args, **kargs):
        super(CommentReplyForm, self).__init__(instance, *args, **kargs)
        self.instance = instance
        self.user = user
        self.question = instance["question_id"]
        self.description = instance["description"]

    def __process__(self):
        return Business.comment_reply(self.cleaned_data, self.user, self.question)


class EditAnswerForm(IdeiaModelForm):
    description = forms.CharField(max_length=2048, required=True)

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