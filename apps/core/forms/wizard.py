# coding=utf-8
from apps.custom_base.service.custom import IdeiaForm
from apps.geography.models import State, City
from apps.userprofile.models import Responsibility, GenderType
from django import forms
from django.conf import settings
from django.utils.translation import ugettext as _
from ..business import user as UserBusiness
from apps.userprofile.service import business as BusinessUserProfile
from django.core.exceptions import ValidationError
from django.utils import timezone


class WizardForm(IdeiaForm):

    user = None

    def __init__(self, data=None, files=None, user=None, *args, **kwargs):

        self.user = user
        super(WizardForm, self).__init__(data=data, files=files, *args, **kwargs)


class StepOneWizardForm(WizardForm):

    responsibility = forms.ModelChoiceField(queryset=Responsibility.objects.all(), required=True)
    state = forms.ModelChoiceField(queryset=State.objects.filter(country=1), required=False)
    birth = forms.DateField(input_formats=['%d/%m/%Y'], required=True)
    gender = forms.ChoiceField(choices=GenderType.CHOICES, required=True)
    city_hometown = forms.ModelChoiceField(queryset=City.objects.all(), required=True)
    profile_picture = forms.ImageField(required=False)
    wizard_step = forms.IntegerField(required=True)

    def __init__(self, data=None, files=None, user=None, *args, **kwargs):

        initial = kwargs.get('initial', {})

        if user and hasattr(user, 'user_profile'):
            initial = self.load_initial_data(user, initial)

        kwargs.update({
            'initial': initial
        })

        kwargs.update({
            'user': user
        })

        super(StepOneWizardForm, self).__init__(data, files, *args, **kwargs)

        #if 'city_hometown' in initial:
            #self.fields['city_hometown'].queryset = City.objects.filter(id=initial.get('city_hometown').id)

    def load_initial_data(self, user, initial):

        if user.user_profile.city_hometown:
            initial.update({
                'state': user.user_profile.city_hometown.state,
                'city_hometown': user.user_profile.city_hometown,
            })

        if user.user_profile.birth:
            initial.update({
                'birth': user.user_profile.birth
            })

        print(user.user_profile.current_occupation)

        if user.user_profile.current_occupation:
            initial.update({
                'responsibility': user.user_profile.current_occupation.responsibility
            })

        if user.user_profile.gender:
            initial.update({
                'gender': user.user_profile.gender
            })

        return initial

    def is_valid(self):

        is_valid = super(StepOneWizardForm, self).is_valid()
        image = self.cleaned_data.get('profile_picture', False)
        birth = self.cleaned_data.get('birth', None)

        if birth and birth.year > timezone.now().year:
            is_valid = False
            self.add_error('birth', ValidationError(_('Birth invalid.'), code='birth'))

        if 'gender' in self.cleaned_data:
            if self.cleaned_data['gender'].upper() not in ['M', 'F']:
                is_valid = False
                self.add_error('gender',
                               ValidationError(_('Gênero não permitido.'), code='gender'))

        if image and 'image' in self.changed_data:
            if image.content_type not in getattr(settings, 'IMAGES_ALLOWED'):
                self.add_error('profile_picture',
                               ValidationError(_('Image format is not allowed.'), code='profile_picture'))
                is_valid = False

            if image._size > 1024 * 1024:
                self.add_error('profile_picture',
                               ValidationError(_('Image size more than 1mb.'), code='profile_picture'))
                is_valid = False

        return is_valid

    def __process__(self):

        process_profile = BusinessUserProfile.edit_profile(self.user, self.cleaned_data)
        process_occupation = BusinessUserProfile.update_or_create_occupation(
            process_profile,
            responsibilities=[self.cleaned_data.get('responsibility')])

        return process_profile if (process_profile and process_occupation) else False


class StepTwoWizardForm(WizardForm):

    pass