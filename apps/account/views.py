from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.utils.decorators import method_decorator
from django.views.decorators.http import require_POST
from django.views.generic import View
from .service.forms import SignUpForm, LoginForm, ChangePasswordForm, RecoveryPasswordForm, ForgotPasswordForm, \
    ResendAccountConfirmationForm
from .service.business import log_in_user, logout_user, register_confirm, check_token_exist
from django.utils.translation import ugettext as _


class IndexView(View):

    template_name = 'account/index.html'

    @method_decorator(login_required)
    def get(self, request):
        """
        Show the index page

        :param request:
        :return: HTML
        """
        return render(request, self.template_name)


class LoginView(View):

    def get(self, request):
        """
        Show the login form page

        :param request:
        :return: HTML
        """

        url_next = '/account/'

        if 'next' in request.GET and request.GET['next']:
            url_next = request.GET['next']

        if not request.user.is_authenticated():
            form = LoginForm()
            return render(request, 'account/login.html', {form: form})
        else:
            return redirect(url_next)

    def post(self, request):
        """
        Method processing trigger the login box

        :param request:
        :return:
        """

        url_next = '/account/'

        if 'next' in request.GET and request.GET['next']:
            url_next = request.GET['next']

        form = LoginForm(request, request.POST)
        if form.process():
            url_next = '/profile/feed/' if form.redirect_to_wizard else url_next
            return redirect(url_next)

        return render(request, 'account/login.html', {'form': form})


class LogoutView(View):


    def get(self, request):
        """
        Action to logout user

        :param request:
        :return:
        """
        logout_user(request)
        return redirect('/account/')


class RegisterView(View):

    def get(self, request):
        """
        Show the sign-up form

        :param request:
        :return: HTML
        """
        if request.user.is_authenticated():
            return redirect('/')
        else:
            form = SignUpForm()
            return render(request, 'account/signup.html', {form: form})

    def post(self, request):
        """
        Action to register new user

        :param request:
        :return: HTML
        """
        form = SignUpForm(request.POST)
        if form.process():
            messages.add_message(request, messages.SUCCESS, _("Success"))
            return redirect('/account/registered-successfully')

        return render(request, 'account/signup.html', {'form': form})


class RegisteredSucessView(View):

    def get(self, request):
        """
        Show the success message

        :param request:
        :return:
        """
        message = _("Registered Successfully")
        return render(request, 'account/registered_successfully.html', {'message': message})


class MailValidationView(View):

    def get(self, request, activation_key):
        """
        Method for validate url with token sent by email to confirm user's account

        :param request:
        :param activation_key:
        :return: HTML
        """

        message = _('Token not exist')

        try:
            register_confirm(activation_key)
            message = _('Token exist - Account verified')
        except Exception as e:
            message = e.message

        return render(request, 'account/mail_validation.html', {'message': message})


class RecoveryValidationView(View):

    def get(self, request, activation_key = None):
        """
        Method to validate url with the token sent by email to the user to change the password

        :param request:
        :param activation_key:
        :return: HTML
        """

        message = 'Token not exist'

        token = check_token_exist(activation_key)
        if token and token.is_active() and token.is_valid():
            form = RecoveryPasswordForm()
            return render(request, 'account/password_recovery.html', {'form': form, 'activation_key': activation_key})

        return render(request, 'account/recovery_validation.html', {'message': message})

    def post(self, request, activation_key):
        """
        Method to validate url with the token sent by email to the user to change the password

        :param request:
        :return: HTML
        """

        message = _('Token not exist')

        token = check_token_exist(request.POST['activation_key'])
        if token and token.is_active() and token.is_valid():
            form = RecoveryPasswordForm(token, request.POST)

            if form.process():
                message = _('Password successfully changed!')
                return render(request, 'account/password_recovery_successfully.html', {'message': message})

            return render(request, 'account/password_recovery.html', {
                'form': form,
                'activation_key': request.POST['activation_key']
            })

        return render(request, 'account/recovery_validation.html', {'form'})



class ChangePasswordView(View):

    @method_decorator(login_required)
    def get(self, request):
        """
        Show the change password form

        :param request:
        :return: HTML
        """
        form = ChangePasswordForm()
        return render(request, 'account/password_change.html', {'form': form})

    @method_decorator(login_required)
    def post(self, request):
        """
        Action to update password

        :param request:
        :return:
        """
        form = ChangePasswordForm(request.user, request.POST)
        if form.process():
            return render(request, 'account/password_change_successfully.html')

        return render(request, 'account/password_change.html', {'form': form})


class ForgotPasswordView(View):

    def get(self, request):
        form = ForgotPasswordForm()
        return render(request, 'account/password_forgot.html', {'form': form})

    def post(self, request):
        """
        Method to process form of

        :param request:
        :return:
        """
        form = ForgotPasswordForm(request.POST)
        if form.process():
            message = _('A confirmation email was sent to you')
            return render(request, 'account/password_sent_email_successfully.html', {'message': message})

        return render(request, 'account/password_forgot.html', {'form': form})


class ResendAccountConfirmationView(View):

    def get(self, request):
        form = ResendAccountConfirmationForm()
        return render(request, 'account/resend_account_confirmation.html', {'form': form})


    def post(self, request):
        form = ResendAccountConfirmationForm(request.POST)
        if form.process():
            message = 'E-mail re-sent successfully!'
            return render(request, 'account/resend_account_confirmation_successfully.html', {'message': message})

        return render(request, 'account/resend_account_confirmation.html', {'form': form})