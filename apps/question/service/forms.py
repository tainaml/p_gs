from django.core.exceptions import ValidationError
from django.db import models
from custom_forms.custom import forms, IdeiaForm
import business as Business
from django.conf import settings


class CreateQuestionForm(IdeiaForm):
    title = forms.CharField(max_length=256, required=True)
    description = forms.CharField(max_length=2048, required=True)

    def __init__(self, data, user=None, question=None, *args, **kargs):
        self.question = question
        self.user = user
        super(CreateQuestionForm, self).__init__(data, *args, **kargs)

    def is_valid(self):
        is_valid = super(CreateQuestionForm, self).is_valid()
        return is_valid

    def __process__(self):
            return Business.save_question(self.user, self.cleaned_data)


class EditQuestionForm(IdeiaForm):
    title = forms.CharField(max_length=256, required=True)
    description = forms.CharField(max_length=2048, required=True)

    def __init__(self, instance=None, *args, **kargs):
        super(EditQuestionForm, self).__init__(*args, **kargs)
        self.instance = instance if instance and isinstance(instance, models.Model) else None

    def is_valid(self):
        is_valid = super(EditQuestionForm, self).is_valid()
        return is_valid

    def __process__(self):
        return Business.update_question(self.cleaned_data, self.instance)