# coding=utf-8
from django.db.models import Q
from apps.account.models import User
from apps.account.service.forms import BaseSignupForm
from apps.custom_base.service.custom import IdeiaForm
from apps.geography.models import State, City
from apps.userprofile.models import Responsibility, GenderType
from django import forms
from django.conf import settings
from django.utils.translation import ugettext as _
from apps.userprofile.service import business as BusinessUserProfile
from django.core.exceptions import ValidationError
from django.utils import timezone


class WizardForm(IdeiaForm):

    user = None

    def __init__(self, data=None, files=None, user=None, *args, **kwargs):

        self.user = user
        super(WizardForm, self).__init__(data=data, files=files, *args, **kwargs)


class StepOneWizardForm(BaseSignupForm, WizardForm):


    responsibility = forms.ModelChoiceField(queryset=Responsibility.objects.filter(avaiable_to_choose=True), required=False)
    state = forms.ModelChoiceField(queryset=State.objects.filter(country=1), required=False)
    birth = forms.DateField(input_formats=['%d/%m/%Y'], required=True)
    gender = forms.ChoiceField(choices=GenderType.CHOICES, required=True)
    city = forms.ModelChoiceField(queryset=City.objects.all(), required=True)
    profile_picture = forms.ImageField(required=False)
    wizard_step = forms.IntegerField(required=True)

    def clean_email(self):
        return self.user.email if self.user.email else super(StepOneWizardForm, self).clean_email()

    def is_email_valid(self, valid):

        if 'email' in self.cleaned_data and User.objects.filter(Q(email=self.cleaned_data['email']) & ~Q(id=self.user.id)).exists():
            self.add_error('email', ValidationError(_('Email is already in use.'), code='email'))
            valid = False

        return valid

    def __init__(self, data=None, files=None, user=None, *args, **kwargs):

        self.initial = {
            'first_name': user.first_name,
            'last_name': user.last_name,
            'email': user.email
        }

        self.initial.update(kwargs.get('initial', {}))

        if user.email:
            self.declared_fields['email'].required = False

        if user and hasattr(user, 'user_profile'):
            self.initial = self.load_initial_data(user, self.initial)

        kwargs.update({
            'initial': self.initial
        })

        kwargs.update({
            'user': user
        })

        super(StepOneWizardForm, self).__init__(data, files, *args, **kwargs)


    def load_initial_data(self, user, initial):

        if user.user_profile.city:
            initial.update({
                'state': user.user_profile.city.state,
                'city': user.user_profile.city,
            })

        if user.user_profile.birth:
            initial.update({
                'birth': user.user_profile.birth
            })

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

        # TODO: Remove this POG
        responsibility = self.cleaned_data.get('responsibility', None)
        if not responsibility:
            is_valid = False
            self.add_error('responsibility', ValidationError(u'Este campo é obrigatório', code='responsibility'))

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