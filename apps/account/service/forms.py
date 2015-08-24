from django.contrib.auth.models import User
from nocaptcha_recaptcha import NoReCaptchaField
import business as Business
__author__ = 'phillip'
from django import forms


class SignUpForm(forms.Form):

    username = forms.CharField(max_length=100, required=True)
    first_name = forms.CharField(max_length=30, required=True)
    last_name = forms.CharField(max_length=150, required=True)
    email = forms.EmailField(max_length=150, required=True)
    password = forms.CharField(max_length=50, required=True)
    password_confirmation = forms.CharField(max_length=50, required=True)
    captcha = NoReCaptchaField(required=True)

    def clean(self):
        cleaned_data = super(SignUpForm, self).clean()
        if cleaned_data.has_key('password') and cleaned_data.has_key('password_confirmation') and \
                        cleaned_data['password'] != cleaned_data['password_confirmation']:
            raise forms.ValidationError({'password': ["Passwords are not the same."]})

        if cleaned_data.has_key('username') and User.objects.filter(username=cleaned_data['username']).exists():
            raise forms.ValidationError({'username': ["Username is already in use."]})

    def save(self):
        try:

            return Business.register_user(self.cleaned_data) if self.is_valid() \
                else False
        except:

            self.add_error(None, "General error")
