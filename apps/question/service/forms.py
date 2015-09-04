from django.core.exceptions import ValidationError
from custom_forms.custom import forms, IdeiaForm
import business as Business
from django.conf import settings


class CreateQuestionForm(IdeiaForm):
    title = forms.CharField(max_length=256, required=True)
    description = forms.CharField(max_length=2048, required=True)

    def __init__(self, question=None, *args, **kargs):
        self.question = question
        super(CreateQuestionForm, self).__init__(*args, **kargs)


    def __process__(self):
        return Business.save_question(self.question, self.cleaned_data)

    def is_valid(self):

        return True