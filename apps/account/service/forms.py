from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from nocaptcha_recaptcha import NoReCaptchaField

import business as Business
from custom_forms.custom import forms, IdeiaForm


class SignUpForm(IdeiaForm):
    username = forms.CharField(max_length=100, required=True)
    first_name = forms.CharField(max_length=30, required=True)
    last_name = forms.CharField(max_length=150, required=True)
    email = forms.EmailField(max_length=150, required=True)
    password = forms.CharField(max_length=50, required=True)
    password_confirmation = forms.CharField(max_length=50, required=True)
    captcha = NoReCaptchaField(required=True)

    def is_valid(self):
        valid = super(SignUpForm, self).is_valid()

        if 'password' in self.cleaned_data and 'password_confirmation' in self.cleaned_data and \
                        self.cleaned_data['password'] != self.cleaned_data['password_confirmation']:
            forms.add_error({'password': ValidationError('Passwords are not the same.', code='password')})
            valid = False

        if 'username' in self.cleaned_data and User.objects.filter(username=self.cleaned_data['username']).exists():
            forms.add_error({'username': ValidationError('Username is already in use.', code='username')})
            valid = False

        if 'email' in self.cleaned_data and User.objects.filter(email=self.cleaned_data['email']).exists():
            forms.add_error({'email': ValidationError('Email is already in use.', code='email')})
            valid = False

        return valid

    def __process__(self):
        return Business.register_user(self.cleaned_data)


class LoginForm(forms.Form):
    username = forms.CharField(max_length=100, required=True)
    password = forms.CharField(max_length=50, required=True)

    def clean(self):
        cleaned_data = super(LoginForm, self).clean()
        if 'password' in cleaned_data and 'username' in cleaned_data:
            user = Business.authenticate_user(username_or_email=cleaned_data['username'],
                                              password=cleaned_data['password'])
            if not user:
                raise forms.ValidationError({'password': ["Wrong password or username."]})
            else:
                self.instance = user


class ChangePasswordForm(forms.Form):
    old_password = forms.CharField(max_length=30, required=True)
    new_password = forms.CharField(max_length=30, required=True)
    new_password_confirmation = forms.CharField(max_length=30, required=True)

    def __init__(self, user=None, *args, **kwargs):
        self.user = user
        super(ChangePasswordForm, self).__init__(*args, **kwargs)

    def clean(self):
        cleaned_data = super(ChangePasswordForm, self).clean()
        if 'old_password' in cleaned_data:
            is_authenticated = Business.authenticate_user(self.user.username, cleaned_data['old_password'])
            if not is_authenticated:
                raise forms.ValidationError({'old_password': ["Wrong old password."]})

            if 'new_password' in cleaned_data and 'new_password_confirmation' in cleaned_data and \
                    cleaned_data['new_password'] != cleaned_data['new_password_confirmation']:
                raise forms.ValidationError({'new_password': ["Passwords are not the same."]})

    def process(self):
        try:
            return Business.update_password(self.user, self.cleaned_data['new_password']) if self.is_valid() \
                else False
        except:
            self.add_error(None, "General error")


class ForgotPasswordForm(forms.Form):

    email = forms.EmailField(max_length=150, required=True)

    def clean(self):
        cleaned_data = super(ForgotPasswordForm, self).clean()
        if 'email' in cleaned_data and not User.objects.filter(email=cleaned_data['email']).exists():
            raise forms.ValidationError({'email': ["Does not exist account with this email."]})

    def process(self):
        try:
            return Business.forgot_password(self.cleaned_data['email']) if self.is_valid() else False
        except:
            self.add_error(None, "General error")


class RecoveryPasswordForm(forms.Form):

    new_password = forms.CharField(max_length=30, required=True)
    new_password_confirmation = forms.CharField(max_length=30, required=True)

    def __init__(self, token=None, *args, **kwargs):

        self.token = token
        super(RecoveryPasswordForm, self).__init__(*args, **kwargs)

    def clean(self):
        cleaned_data = super(RecoveryPasswordForm, self).clean()
        if 'new_password' in cleaned_data and 'new_password_confirmation' in cleaned_data and \
                cleaned_data['new_password'] != cleaned_data['new_password_confirmation']:
            raise forms.ValidationError({'new_password_confirmation': ["Passwords are not the same."]})

        if not self.token or not self.token.is_valid():
            raise forms.ValidationError("Token is no longer valid.")

    def process(self):
        try:
            return Business.recovery_password(self.token, self.cleaned_data['new_password']) if self.is_valid() \
                else False
        except:
            self.add_error(None, "General error")