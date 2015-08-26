from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from nocaptcha_recaptcha import NoReCaptchaField

import business as Business
from custom_forms.custom import forms, IdeiaForm


class SignUpForm(IdeiaForm):
    username = forms.SlugField(max_length=100, required=True)
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
            self.add_error('password', ValidationError('Passwords are not the same.', code='password'))
            valid = False

        if 'username' in self.cleaned_data and User.objects.filter(username=self.cleaned_data['username']).exists():
            self.add_error('username', ValidationError('Username is already in use.', code='username'))
            valid = False

        if 'email' in self.cleaned_data and User.objects.filter(email=self.cleaned_data['email']).exists():
            self.add_error('email', ValidationError('Email is already in use.', code='email'))
            valid = False

        return valid

    def __process__(self):
        return Business.register_user(self.cleaned_data)


class LoginForm(IdeiaForm):
    username = forms.CharField(max_length=100, required=True)
    password = forms.CharField(max_length=50, required=True)

    def __init__(self, request=None, *args, **kwargs):
        self.request = request
        super(LoginForm, self).__init__(*args, **kwargs)

    def is_valid(self):
        valid = super(LoginForm, self).is_valid()

        if 'password' in self.cleaned_data and 'username' in self.cleaned_data:
            self.instance = Business.authenticate_user(username_or_email=self.cleaned_data['username'],
                                                       password=self.cleaned_data['password'])
            if not self.instance:
                self.add_error('password', ValidationError('Wrong password or username.', code='password'))
                valid = False
            else:
                if self.instance.is_active is False:
                    self.add_error(None, ValidationError('Account is not active',
                                                         code='account_not_active'))
                    valid = False
                    self.account_is_active = False
                    self.account_is_active_errors = 'Account is not active'

        return valid

    def __process__(self):

        return Business.log_in_user(self.request, self.instance)


class ChangePasswordForm(IdeiaForm):
    old_password = forms.CharField(max_length=30, required=True)
    new_password = forms.CharField(max_length=30, required=True)
    new_password_confirmation = forms.CharField(max_length=30, required=True)

    def __init__(self, user=None, *args, **kwargs):
        self.user = user
        super(ChangePasswordForm, self).__init__(*args, **kwargs)

    def is_valid(self):
        valid = super(ChangePasswordForm, self).is_valid()

        if 'old_password' in self.cleaned_data:
            is_authenticated = Business.authenticate_user(self.user.username, self.cleaned_data['old_password'])
            if not is_authenticated:
                self.add_error('old_password', ValidationError('Wrong old password.', code='old_password'))
                valid = False

            if 'new_password' in self.cleaned_data and 'new_password_confirmation' in self.cleaned_data and \
                    self.cleaned_data['new_password'] != self.cleaned_data['new_password_confirmation']:
                self.add_error('new_password', ValidationError('Passwords are not the same.', code='new_password'))
                valid = False

        return valid

    def __process__(self):
        return Business.update_password(self.user, self.cleaned_data['new_password'])


class ForgotPasswordForm(IdeiaForm):
    email = forms.EmailField(max_length=150, required=True)

    def is_valid(self):
        valid = super(ForgotPasswordForm, self).is_valid()

        if 'email' in self.cleaned_data and not User.objects.filter(email=self.cleaned_data['email']).exists():
            self.add_error('email', ValidationError('Does not exist account with this email.', code='email'))
            valid = False

        return valid

    def __process__(self):
        return Business.forgot_password(self.cleaned_data['email']) if self.is_valid() else False


class RecoveryPasswordForm(IdeiaForm):
    new_password = forms.CharField(max_length=30, required=True)
    new_password_confirmation = forms.CharField(max_length=30, required=True)

    def __init__(self, token=None, *args, **kwargs):
        self.token = token
        super(RecoveryPasswordForm, self).__init__(*args, **kwargs)

    def is_valid(self):
        valid = super(RecoveryPasswordForm, self).is_valid()

        if 'new_password' in self.cleaned_data and 'new_password_confirmation' in self.cleaned_data and \
                self.cleaned_data['new_password'] != self.cleaned_data['new_password_confirmation']:
            self.add_error('new_password_confirmation', ValidationError('Passwords are not the same.',
                                                                        code='new_password_confirmation'))
            valid = False

        if not self.token or not self.token.is_valid():
            self.add_error('password', ValidationError('Token is no longer valid.', code='password'))
            valid = False

        return valid

    def __process__(self):
        return Business.recovery_password(self.token, self.cleaned_data['new_password'])
