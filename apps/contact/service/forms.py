from django.core.exceptions import ValidationError
from django.utils.translation import ugettext as _
from nocaptcha_recaptcha import NoReCaptchaField

from custom_forms.custom import IdeiaForm, forms
import business as Business


class ContactForm(IdeiaForm):
    subject = forms.ModelChoiceField(queryset=Business.get_contact_subjects(), required=True)
    message = forms.CharField(max_length=1024, required=True)

    def __init__(self, user=None, *args, **kwargs):
        self.user = user
        super(ContactForm, self).__init__(*args, **kwargs)

    def __process__(self):
        self.instance = Business.save(self.cleaned_data, self.user)
        return self.instance


class ContactFormNoAuthenticated(ContactForm):

    name = forms.CharField(max_length=100, required=True)
    email = forms.EmailField(required=True)
    captcha = NoReCaptchaField(required=True)

    def __process__(self):
        return super(ContactFormNoAuthenticated, self).__process__()
