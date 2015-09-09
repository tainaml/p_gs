from django.db import models
from django.core.validators import RegexValidator
import pickle
from apps.userprofile.models import City
import business as Business
from django.core.exceptions import ValidationError
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
    profile_picture = forms.ImageField(required=False)

    def __init__(self, user=None, data_model=None, *args, **kwargs):
        self.user = user
        self.data_model = data_model

        super(EditProfileForm, self).__init__(*args, **kwargs)

        if self.data and 'state' in self.data:
            self.fields['city'].queryset = City.objects.filter(state=self.data['state'])

    def is_valid(self):

        is_valid = super(EditProfileForm, self).is_valid()
        image = self.cleaned_data.get('profile_picture', False)
        if image:
            if image._size > 1024 * 1024:
                self.add_error('profile_picture', ValidationError(_('Image size more than 1mb.'), code='profile_picture'))
                is_valid = False


        return is_valid



    def __process__(self):
        return Business.edit_profile(self.user, self.cleaned_data, None)



class OccupationForm(IdeiaForm):

    responsibility = forms.CharField(max_length=100)
    description = forms.CharField(max_length=100)

    def __init__(self, data=None, request=None, data_model=None, instance=None, *args, **kwargs):
        self.request = request
        self.instance = instance if instance and isinstance(instance, models.Model) else None

        super(OccupationForm, self).__init__(data, *args, **kwargs)

        if data_model is not None and isinstance(data_model, models.Model):
            self.data = forms.model_to_dict(data_model)

    def is_valid(self):
        is_valid = super(OccupationForm, self).is_valid()
        return is_valid

    def __process__(self):
        if self.instance:
            return Business.update_occupation(self.instance, self.cleaned_data)
        else:
            return Business.create_occupation(self.request.user, self.cleaned_data)