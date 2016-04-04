from django import forms
from django.core.exceptions import ValidationError
from django.utils.translation import ugettext as _

from apps.account.models import User
from apps.custom_base.service.custom import IdeiaForm
from apps.account.service.business import deactivate_account


class CoreDeactivateAccountForm(IdeiaForm):

    user = forms.ModelChoiceField(queryset='')

    def __init__(self, request=None, *args, **kwargs):
        self.request = request
        super(CoreDeactivateAccountForm, self).__init__(*args, **kwargs)
        self.fields['user'].queryset = User.objects.filter(id=self.request.user.id)
        
    def is_valid(self):
        is_valid = super(CoreDeactivateAccountForm, self).is_valid()

        if 'user' not in self.cleaned_data or self.cleaned_data.get('user') != self.request.user:
            self.add_error(None, ValidationError(_('Ocorreu um erro ao desativar a conta'), code='invalid-user'))
            is_valid = False

        return is_valid

    def __process__(self):
        return deactivate_account(
            self.request,
            self.cleaned_data.get('user')
        )



