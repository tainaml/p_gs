from apps.custom_base.service.custom import IdeiaForm, forms
from django.conf import settings
__author__ = 'phillip'

class WizardBase(IdeiaForm):
    step = forms.IntegerField(max_value=settings.WIZARD_STEPS_TOTAL)


class WizardFormStepOne(WizardBase):
    pass