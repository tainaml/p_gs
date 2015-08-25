from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from django.views.decorators.http import require_POST
from .service.forms import SignUpForm, LoginForm, ChangePasswordForm
from .service.business import log_in_user, logout_user, register_confirm, check_token_exist

 

def login(request):

    form = LoginForm()
    return render(request, 'account/login.html', {form: form})

@require_POST
def do_login(request):

    form = LoginForm(request.POST)
    if form.is_valid():
        log_in_user(request, form.instance)

        return redirect('/')

    return render(request, 'account/login.html', {'form': form})

def logout(request):

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


def signup_without_captcha(request):
    if request.user.is_authenticated():
        return redirect('/')
    else:
        form = SignUpForm()

        return render(request, '../templates/account/signup_without_captcha.html', {form: form})


@require_POST
def register(request):
    """
    Action to register new user
    :param request:
    :return: HTML
    """
    form = SignUpForm(request.POST)
    if form.save():
        messages.add_message(request, messages.SUCCESS, "Success")
        return redirect('/account/registered-successfully')


    return render(request, 'account/signup.html', {'form': form})


def registered_successfully(request):

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
    if token:
        message = 'Token exist'

    return render(request, 'account/recovery_validation.html', {'message': message})

@login_required
def change_password(request):

    form = ChangePasswordForm()

    return render(request, 'account/password_change.html', {'form': form})

def update_password(request):

    form = ChangePasswordForm(request.user, request.POST)
    if form.process():
        return render(request, 'account/password_change_successfully.html')

    return render(request, 'account/password_change.html', {'form': form})