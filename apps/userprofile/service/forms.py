from django.db import models
from apps.userprofile.models import City, Country, State
import business as Business

from django.contrib.auth.models import User
from django.utils.translation import ugettext as _

from custom_forms.custom import forms, IdeiaForm


class EditProfileForm(IdeiaForm):

    birth = forms.DateField(input_formats=['%d/%m/%Y'], )
    gender = forms.CharField(max_length=1)
    city = forms.ModelChoiceField(queryset='')

    def __init__(self, data=None, request=None, data_model=None, set_queryset=None, *args, **kwargs):
        self.request = request

        super(EditProfileForm, self).__init__(data, *args, **kwargs)

        if self.data and 'state' in self.data:
            self.fields['city'].queryset = City.objects.filter(state=self.data['state'])

        if data_model is not None and isinstance(data_model, models.Model):
            self.data = forms.model_to_dict(data_model)

    def is_valid(self):
        is_valid = super(EditProfileForm, self).is_valid()

        return is_valid

    def __process__(self):
        return Business.update_profile(self.request.user, self.cleaned_data)