from django.core.exceptions import ValidationError
from nocaptcha_recaptcha import NoReCaptchaField
from django.utils.translation import ugettext as _

from custom_forms.custom import IdeiaForm, forms
import business as Business


class ContactForm(IdeiaForm):

    name = forms.CharField(max_length=100, required=False)
    email = forms.EmailField(required=False)
    subject = forms.ModelChoiceField(queryset=Business.get_contact_subjects(), required=True)
    message = forms.CharField(max_length=1024, required=True)
    captcha = NoReCaptchaField(required=True)

    def __init__(self, user=None, *args, **kargs):
        self.user = user
        super(ContactForm, self).__init__(*args, **kargs)

    def is_valid(self):

        is_valid = super(ContactForm, self).is_valid()

        if self.user.is_authenticated() and self.cleaned_data['subject'] is not '' and self.cleaned_data['message'] is not '':
            return True

        if not self.user.is_authenticated() and not self.cleaned_data['name'] :
            self.add_error('name', ValidationError(_('This field is required.'), code='name'))
            is_valid = False

        if not self.user.is_authenticated() and not self.cleaned_data['email']:
            self.add_error('email', ValidationError(_('This field is required.'), code='email'))
            is_valid = False

        return is_valid

    def __process__(self):
        self.instance = Business.save(self.cleaned_data, self.user)
        return self.instance
