from django.contrib import messages
from django.http import Http404
from django.shortcuts import render, redirect
from django.views.decorators.http import require_POST
from .service.forms import SignUpForm, LoginForm
from .service.business import log_in_user, logout_user

def login(request):

    form = LoginForm()
    return render(request, 'account/login.html', {form: form})

@require_POST
def do_login(request):

    form = LoginForm(request.POST)
    if form.is_valid():
        log_in_user(request, form.instance)

        return redirect('/')

    # is not working show form errors directyle in view. Is it a bug? =(
    return render(request, 'account/login.html', context={form: form, 'errors': form.errors})

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