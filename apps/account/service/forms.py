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

class LoginForm(forms.Form):
    username = forms.CharField(max_length=100, required=True)
    password = forms.CharField(max_length=50, required=True)

    def clean(self):
        cleaned_data = super(LoginForm, self).clean()
        if cleaned_data.has_key('password') and cleaned_data.has_key('username'):
            user = Business.authenticate_user(username_or_email=cleaned_data['username'], password=cleaned_data['password'])
            if not user:
                raise forms.ValidationError({'password': ["Wrong password or username."]})
            else:
                self.instance=user

class ChangePasswordForm(forms.Form):
    old_password = forms.CharField(max_length=30, required=True)
    new_password = forms.CharField(max_length=30, required=True)
    new_password_confirmation = forms.CharField(max_length=30, required=True)

    def __init__(self, user=None, *args, **kwargs):
        self.user = user
        super(ChangePasswordForm, self).__init__(*args, **kwargs)


    def clean(self):
        cleaned_data = super(ChangePasswordForm, self).clean()
        if cleaned_data.has_key('old_password'):
            is_authenticated = Business.authenticate_user(self.user.username, cleaned_data['old_password'])
            if not is_authenticated:
                raise forms.ValidationError({'old_password': ["Wrong old password."]})

            if cleaned_data.has_key('new_password') and cleaned_data.has_key('new_password_confirmation') and \
                        cleaned_data['new_password'] != cleaned_data['new_password_confirmation']:
                raise forms.ValidationError({'new_password': ["Passwords are not the same."]})

    def process(self):

        try:
            return Business.update_password(self.user, self.cleaned_data['new_password']) if self.is_valid() \
                else False
        except:

            self.add_error(None, "General error")








