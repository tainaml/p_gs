from django.core.exceptions import ValidationError

__author__ = 'phillip'
from custom_forms.custom import forms, IdeiaForm
from django.conf import settings
from business import count_actions_by_user_and_action

class UserCountForm(IdeiaForm):
    action = forms.CharField(required=True)

    def __init__(self, user=None, *args, **kargs):
        self.user = user
        super(UserCountForm, self).__init__(*args, **kargs)

    def is_valid(self):
        valid = super(UserCountForm, self).is_valid()

        if 'action' in self.cleaned_data and \
                        self.cleaned_data['action'] not in settings.SOCIAL_LABELS.values():
            valid = False
            self.add_error(None,
                           ValidationError(('action not found.'),
                                           code='action_not_found'))

        return valid

    def __process__(self):
        return count_actions_by_user_and_action(self.user, action=self.cleaned_data['action'])
