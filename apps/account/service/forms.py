# coding=utf-8
from django.contrib.auth import get_user_model
from apps.account.models import User
from django.core.exceptions import ValidationError
from nocaptcha_recaptcha import NoReCaptchaField
from django.utils.translation import ugettext as _
from apps.account.models import User

import business as Business
from apps.custom_base.service.custom import forms, IdeiaForm
from rede_gsti import settings


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
            self.add_error('password', ValidationError(_('Passwords are not the same.'), code='password'))
            valid = False

        if 'username' in self.cleaned_data and User.objects.filter(username=self.cleaned_data['username']).exists():
            self.add_error('username', ValidationError(_('Username is already in use.'), code='username'))
            valid = False

        if 'email' in self.cleaned_data and User.objects.filter(email=self.cleaned_data['email']).exists():
            self.add_error('email', ValidationError(_('Email is already in use.'), code='email'))
            valid = False

        return valid

    def __process__(self):
        return Business.register_user(self.cleaned_data)


class LoginForm(IdeiaForm):
    username = forms.CharField(max_length=100, required=True)
    password = forms.CharField(max_length=50, required=True)

    instance = None

    def __init__(self, request=None, *args, **kwargs):
        self.request = request
        self.redirect_to_wizard = False
        super(LoginForm, self).__init__(*args, **kwargs)

    def is_valid(self):
        valid = super(LoginForm, self).is_valid()

        if 'password' in self.cleaned_data and 'username' in self.cleaned_data:
            self.instance = Business.authenticate_user(username_or_email=self.cleaned_data.get('username'),
                                                       password=self.cleaned_data.get('password'))

            if not self.instance:
                self.add_error(None, ValidationError(_('Wrong password or username.'), code='password'))
                valid = False
            else:
                if self.instance.is_active is False:
                    # url = reverse('account:resend_account_confirmation')
                    # btn = '<a href="%s" ' \
                    #       'data-toggle="modal" ' \
                    #       'data-target="#modal-resend-email-confirmation">%s</a>' % (url, _('click here'))
                    #
                    # error = _('Account is not active.')
                    # error += '<br>'
                    # error += _('If you have not received the confirmation email %s to resend.') % btn

                    # self.add_error(None, ValidationError(error, code='account_not_active'))
                    self.account_is_active = False
                    valid = False
                else:
                    self.account_is_active = True

            if self.instance and self.instance.profile and self.instance.profile.wizard_step < settings.WIZARD_STEPS_TOTAL:
                self.redirect_to_wizard = True

        return valid

    def __process__(self):
        return Business.log_in_user(self.request, self.instance)


class ChangePasswordForm(IdeiaForm):
    old_password = forms.CharField(max_length=30, required=True)
    new_password = forms.CharField(max_length=30, required=True)
    new_password_confirmation = forms.CharField(max_length=30, required=True)

    def __init__(self, request=None, *args, **kwargs):
        self.request = request
        self.user = request.user
        super(ChangePasswordForm, self).__init__(*args, **kwargs)

    def is_valid(self):
        valid = super(ChangePasswordForm, self).is_valid()

        if 'old_password' in self.cleaned_data:
            is_authenticated = Business.authenticate_user(self.user.username, self.cleaned_data['old_password'])
            if not is_authenticated:
                self.add_error('old_password', ValidationError(_('Wrong old password.'), code='old_password'))
                valid = False

            if 'new_password' in self.cleaned_data and 'new_password_confirmation' in self.cleaned_data and \
                            self.cleaned_data['new_password'] != self.cleaned_data['new_password_confirmation']:
                self.add_error('new_password', ValidationError(_('Passwords are not the same.'), code='new_password'))
                valid = False

        return valid

    def __process__(self):
        return Business.update_password(
            self.request,
            self.user,
            self.cleaned_data['new_password']
        )


class ForgotPasswordForm(IdeiaForm):
    email = forms.EmailField(max_length=150, required=True)

    def is_valid(self):
        valid = super(ForgotPasswordForm, self).is_valid()

        if 'email' in self.cleaned_data and not User.objects.filter(email=self.cleaned_data['email']).exists():
            self.add_error('email', ValidationError(_('Does not exist account with this email.'), code='email'))
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
            self.add_error('new_password_confirmation', ValidationError(_('Passwords are not the same.'),
                                                                        code='new_password_confirmation'))
            valid = False

        if not self.token or not self.token.is_valid():
            self.add_error('password', ValidationError(_('Token is no longer valid.'), code='password'))
            valid = False

        return valid

    def __process__(self):
        return Business.recovery_password(self.token, self.cleaned_data['new_password'])


class ResendAccountConfirmationForm(IdeiaForm):
    email = forms.EmailField(max_length=150, required=True)

    def is_valid(self):
        valid = super(ResendAccountConfirmationForm, self).is_valid()

        if 'email' in self.cleaned_data and not User.objects.filter(email=self.cleaned_data['email']).exists():
            self.add_error('email', ValidationError('Does not exist account with this email.', code='email'))
            valid = False

        if 'email' in self.cleaned_data and User.objects.filter(email=self.cleaned_data['email'],
                                                                is_active=True).exists():
            self.add_error('email', ValidationError('This account is already active'))
            valid = False

        return valid

    def __process__(self):
        return Business.resend_account_confirmation(self.cleaned_data['email'])


class CheckUsernameForm(IdeiaForm):
    username = forms.CharField(max_length=30, required=True)

    def __process__(self):
        return Business.username_is_available(self.cleaned_data.get('username'))
