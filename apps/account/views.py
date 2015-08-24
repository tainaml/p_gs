from django.contrib import messages
from django.shortcuts import render, redirect
from django.views.decorators.http import require_POST
from .service.forms import SignUpForm


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
    else:
        print form.errors.as_data()

    return render(request, 'account/signup.html', {'form': form})


def registered_successfully(request):
    message = "Registered Successfully"
    return render(request, 'account/registered_successfully.html', {'message': message})