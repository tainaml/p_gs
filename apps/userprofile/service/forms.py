from django.db import models
from django.core.validators import RegexValidator
import pickle
from apps.userprofile.models import City
import business as Business

from django.contrib.auth.models import User
from django.utils.translation import ugettext as _

from custom_forms.custom import forms, IdeiaForm


class MultiWidgetBasic(forms.widgets.MultiWidget):
    def __init__(self, attrs=None):
        widgets = [forms.TextInput(),
                   forms.TextInput()]
        super(MultiWidgetBasic, self).__init__(widgets, attrs)

    def decompress(self, value):
        if value:
            return pickle.loads(value)
        else:
            return ['', '']


class OccupationField(forms.fields.MultiValueField):
    widget = MultiWidgetBasic

    def __init__(self, *args, **kwargs):

        list_fields = [
            forms.CharField(
                error_messages={'incomplete': 'Enter a responsibility.'},
                validators=[RegexValidator(r'^[\w\d](?:[\w\d\s])*$', 'Just text and numbers.')],
                initial="Responsability"
            ),

            forms.CharField(
                error_messages={'incomplete': 'Enter a description of responsibility.'},
                validators=[RegexValidator(r'^[\w\d](?:[\w\d\s])*$', 'Just text and numbers.')],
                initial="Description"
            )
        ]
        super(OccupationField, self).__init__(list_fields, *args, **kwargs)

    def compress(self, values):
        # return pickle.dumps(values)
        return values


class EditProfileForm(IdeiaForm):

    birth = forms.DateField(input_formats=['%d/%m/%Y'])
    gender = forms.CharField(max_length=1)
    city = forms.ModelChoiceField(queryset='')

    def __init__(self, data=None, request=None, data_model=None, data_formset=None, *args, **kwargs):
        self.request = request
        self.formset = data_formset

        super(EditProfileForm, self).__init__(data, *args, **kwargs)

        if self.data and 'state' in self.data:
            self.fields['city'].queryset = City.objects.filter(state=self.data['state'])

        if data_model is not None and isinstance(data_model, models.Model):
            self.data = forms.model_to_dict(data_model)

    def is_valid(self):
        is_valid = super(EditProfileForm, self).is_valid()

        return is_valid

    def __process__(self):
        return Business.edit_profile(self.request.user, self.cleaned_data, None)


class OccupationForm(IdeiaForm):

    responsibility = forms.CharField(max_length=100)
    description = forms.CharField(max_length=100)

    def __init__(self, request=None, *args, **kwargs):
        self.request = request
        super(OccupationForm, self).__init__(*args, **kwargs)

    def is_valid(self):
        is_valid = super(OccupationForm, self).is_valid()
        return is_valid

    def __process__(self):
        return Business.create_occupation(self.request.user, self.cleaned_data)