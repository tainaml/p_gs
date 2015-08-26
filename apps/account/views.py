from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.views.decorators.http import require_POST
from .service.forms import SignUpForm, LoginForm, ChangePasswordForm, RecoveryPasswordForm, ForgotPasswordForm
from .service.business import log_in_user, logout_user, register_confirm, check_token_exist

 
@login_required
def index(request):
    """
    Show the index page

    :param request:
    :return: HTML
    """
    return render(request, 'account/index.html')


def login(request):
    """
    Show the login form page

    :param request:
    :return: HTML
    """
    form = LoginForm()
    return render(request, 'account/login.html', {form: form})


@require_POST
def do_login(request):
    """
    Method processing trigger the login box

    :param request:
    :return:
    """
    form = LoginForm(request.POST)
    if form.is_valid():
        log_in_user(request, form.instance)

        return redirect('/')

    return render(request, 'account/login.html', {'form': form})


def logout(request):
    """
    Action to logout user

    :param request:
    :return:
    """
    logout_user(request)
    return redirect('/')


def signup(request):
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


@require_POST
def register(request):
    """
    Action to register new user

    :param request:
    :return: HTML
    """
    form = SignUpForm(request.POST)
    if form.process():
        messages.add_message(request, messages.SUCCESS, "Success")
        return redirect('/account/registered-successfully')

    return render(request, 'account/signup.html', {'form': form})


def registered_successfully(request):
    """
    Show the success message

    :param request:
    :return:
    """
    message = "Registered Successfully"
    return render(request, 'account/registered_successfully.html', {'message': message})


def mail_validation(request, activation_key):
    """
    Method for validate url with token sent by email to confirm user's account

    :param request:
    :param activation_key:
    :return: HTML
    """

    message = 'Token not exist'

    if register_confirm(activation_key):
        message = 'Token exist - Account verified'

    return render(request, 'account/mail_validation.html', {'message': message})


def recovery_validation(request, activation_key):
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


@login_required
def change_password(request):
    """
    Show the change password form

    :param request:
    :return: HTML
    """
    form = ChangePasswordForm()
    return render(request, 'account/password_change.html', {'form': form})


@require_POST
def update_password(request):
    """
    Action to update password

    :param request:
    :return:
    """
    form = ChangePasswordForm(request.user, request.POST)
    if form.process():
        return render(request, 'account/password_change_successfully.html')

    return render(request, 'account/password_change.html', {'form': form})


def forgot_password(request):

    form = ForgotPasswordForm()
    return render(request, 'account/password_forgot.html', {'form': form})


@require_POST
def do_forgot_password(request):
    """
    Method to process form of

    :param request:
    :return:
    """
    form = ForgotPasswordForm(request.POST)
    if form.process():
        message = 'A confirmation email was sent to you'
        return render(request, 'account/password_sent_email_successfully.html', {'message': message})

    return render(request, 'account/password_forgot.html', {'form': form})


@require_POST
def do_recovery_validation(request):
    """
    Method to validate url with the token sent by email to the user to change the password

    :param request:
    :return: HTML
    """

    message = 'Token not exist'

    token = check_token_exist(request.POST['activation_key'])
    if token and token.is_active() and token.is_valid():
        form = RecoveryPasswordForm(token, request.POST)

        if form.process():
            message = 'Password successfully changed!'
            return render(request, 'account/password_recovery_successfully.html', {'message': message})

        return render(request, 'account/password_recovery.html', {
            'form': form,
            'activation_key': request.POST['activation_key']
        })

    return render(request, 'account/recovery_validation.html', {'form'})