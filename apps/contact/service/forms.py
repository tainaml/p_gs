from django.core.exceptions import ValidationError
from custom_forms.custom import IdeiaForm, forms
from django.utils.translation import ugettext as _
import business as Business


class ContactForm(IdeiaForm):
    SUBJECTS = (
        (0, 'Select'),
        (1, 'Sugest comunity'),
        (2, 'Announce'),
        (3, 'Sugest feature'),
        (4, 'Send bug'),
    )

    name = forms.CharField(max_length=100)
    email = forms.EmailField()
    subject = forms.ChoiceField(choices=SUBJECTS, required=True)
    message = forms.CharField(max_length=1024, required=True)

    def __init__(self, user=None, *args, **kargs):
        self.user = user
        super(ContactForm, self).__init__(*args, **kargs)

    def is_valid(self):

        is_valid = super(ContactForm, self).is_valid()

        if not self.user.is_authenticated and self.cleaned_data['name'] is '':
            self.add_error('name', ValidationError(_('This field is required.'), code='email'))
            is_valid = False
        elif not self.user.is_authenticated and self.cleaned_data['email'] is '':
            self.add_error('email', ValidationError(_('This field is required.'), code='email'))
            is_valid = False

        if self.cleaned_data['subject'] == u'0':
            self.add_error('subject', ValidationError(_('This field is required.'), code='subject'))
            is_valid = False

        return is_valid

    def __process__(self):
        self.instance = Business.save(self.cleaned_data, self.user)
        return self.instance
