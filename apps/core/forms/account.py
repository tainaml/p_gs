from django.db import transaction

from apps.account.service.forms import SignUpForm
from ..business import account as Business


class CoreSignUpForm(SignUpForm):

    @transaction.atomic()
    def __process__(self):
        process_user = super(CoreSignUpForm, self).__process__()
        process_profile = Business.save_profile(process_user)

        return process_user if (process_user and process_profile) else False