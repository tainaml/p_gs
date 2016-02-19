from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.core.urlresolvers import reverse
from django.db import transaction
from django.http import JsonResponse
from django.shortcuts import render, redirect
from django.utils.decorators import method_decorator
from django.views.generic import View
from django.utils.translation import ugettext as _

from rede_gsti import settings
from .service.forms import SignUpForm, LoginForm, ChangePasswordForm, RecoveryPasswordForm, ForgotPasswordForm, \
    ResendAccountConfirmationForm, CheckUsernameForm
from .service.business import logout_user, register_confirm, check_token_exist, log_in_user_no_credentials


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


class IsLogged(View):

    def get(self,request):
        return self.__do__proccess(request)

    def post(self,request):
        return self.__do__proccess(request)

    def __do__proccess(self, request):
        return JsonResponse(data={'is_logged': request.user.is_authenticated()})


class LoginView(View):

    template_path = 'account/login.html'
    form_login = LoginForm

    def return_error(self, request, context=None):
        return render(request, self.template_path, {'form': context['form']})

    def return_success(self, request, context=None):
        return redirect(context['url_next'])

    def get_context(self, request, context=None):
        return {}

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
            form = self.form_login()
            return self.return_error(request, {'form': form})
        else:
            return self.return_success(request, {'url_next': url_next})

    def post(self, request):
        """
        Method processing trigger the login box

        :param request:
        :return:
        """

        url_next = '/account/'

        if 'next' in request.GET and request.GET['next']:
            url_next = request.GET['next']

        form = self.form_login(request, request.POST)

        if form.process():
            url_next = '/profile/feed/' if form.redirect_to_wizard else url_next
            context = {
                'status': 200,
                'url_next': url_next
            }
            return self.return_success(request, context)

        return self.return_error(request, {'form': form})


class LogoutView(View):

    def get(self, request):
        """
        Action to logout user

        :param request:
        :return:
        """
        logout_user(request)
        return redirect('/')


class RegisterView(View):

    form = SignUpForm

    def get(self, request):
        """
        Show the sign-up form

        :param request:
        :return: HTML
        """
        if request.user.is_authenticated():
            return redirect('/')
        else:
            return render(request, 'account/signup.html', {'form': self.form()})

    def post(self, request):
        """
        Action to register new user

        :param request:
        :return: HTML
        """
        form = self.form(request.POST)
        if form.process():
            messages.add_message(request, messages.SUCCESS, _("Success"), 'account-register')
            return redirect('/account/registered-successfully')

        return render(request, 'account/signup.html', {'form': form})


class RegisteredSuccessView(View):

    def get(self, request):
        """
        Show the success message

        :param request:
        :return:
        """
        message = _("Registered Successfully")
        return render(request, 'account/registered_successfully.html', {'message': message})


class RecoveryPasswordSuccessView(View):

    template_message_path = "account/password-message.html"

    def get(self, request):
        """
        Show the success message

        :param request:
        :return:
        """
        message = _("Password successfully recovered")
        return render(request, self.template_message_path, {'message': message, 'icon': 'check'})


class MailValidationView(View):

    @transaction.atomic()
    def get(self, request, activation_key):
        """
        Method for validate url with token sent by email to confirm user's account

        :param request:
        :param activation_key:
        :return: HTML
        """

        message = _('Token not exist')

        try:
            user, token_verified = register_confirm(activation_key)
            message = _('Token exist - Account verified')

            if token_verified and user and user.is_active:

                try:
                    log_in_user_no_credentials(request, user)

                    if user.profile.wizard_step < settings.WIZARD_STEPS_TOTAL:
                        return redirect(reverse('profile:feed'))
                    else:
                        return redirect('/')

                except Exception, e:
                    pass

        except Exception as e:
            message = e.message

        return render(request, 'account/mail_validation.html', {'message': message})


class RecoveryValidationView(View):

    template_path = "account/password-recovery.html"
    template_message_path = "account/password-message.html"

    def get(self, request, activation_key=None):
        """
        Method to validate url with the token sent by email to the user to change the password

        :param request:
        :param activation_key:
        :return: HTML
        """

        message = _('Token not exist!')

        token = check_token_exist(activation_key)
        if token and token.is_active() and token.is_valid():
            form = RecoveryPasswordForm()
            context = {
                'form': form,
                'activation_key': activation_key
            }
            return render(request, self.template_path, context)

        context = {
            'message': message,
            'icon': 'times'
        }
        return render(request, self.template_message_path, context)

    def post(self, request, activation_key):
        """
        Method to validate url with the token sent by email to the user to change the password

        :param request:
        :return: HTML
        """

        message = _('Token not exist!')

        token = check_token_exist(request.POST['activation_key'])
        if token and token.is_active() and token.is_valid():
            form = RecoveryPasswordForm(token, request.POST)
            if form.process():
                message = _('Password successfully changed!')
                context = {
                    'message': message,
                    'icon': 'check'
                }

                if request.is_ajax():
                    return JsonResponse({'url_next': reverse('account:recovery_successfully')}, status=200)
                else:
                    return render(request, self.template_message_path, context)

            if request.is_ajax():
                return JsonResponse({'errors': form.errors}, status=400)
            else:
                return render(request, self.template_path, {
                    'form': form,
                    'activation_key': request.POST['activation_key']
                })

        context = {
            'message': message,
            'icon': 'times'
        }
        return render(request, self.template_message_path, context)


class ChangePasswordView(View):

    form = ChangePasswordForm

    def return_error(self, request, context=None):
        return render(request, 'account/password_change.html', context)

    def return_success(self, request, context=None):
        return render(request, 'account/password_change_successfully.html')

    @method_decorator(login_required)
    def get(self, request):
        """
        Show the change password form

        :param request:
        :return: HTML
        """
        form = self.form()
        return render(request, 'account/password_change.html', {'form': form})

    @method_decorator(login_required)
    def post(self, request):
        """
        Action to update password

        :param request:
        :return:
        """
        form = self.form(request, request.POST)
        if form.process():
            return self.return_success(request)

        return self.return_error(request, {'form': form})


class ForgotPasswordView(View):

    def return_error(self, request, context=None):

        return render(request, 'account/password_forgot.html', context)

    def return_success(self, request, context=None):

        return render(request, 'account/password_sent_email_successfully.html', context)

    def get(self, request):
        form = ForgotPasswordForm()
        return self.return_error(request, {'form': form})

    def post(self, request):
        """
        Method to process form of

        :param request:
        :return:
        """
        form = ForgotPasswordForm(request.POST)
        if form.process():
            message = _('A confirmation email was sent to you')
            return self.return_success(request, {'message': message})

        return self.return_error(request, {'form': form})


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


class CheckUsernameView(View):

    form = CheckUsernameForm

    def get(self, request):

        form = self.form(request.GET)

        if form.process():
            message = _('Username is available!')
            status = 200
            is_available = True
        else:
            message = _('Username is not available!')
            status = 400
            is_available = False

        data = {
            'message': message,
            'status': status,
            'is_available': is_available
        }

        return JsonResponse(data, status=status)
