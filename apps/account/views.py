from django.contrib import messages
from django.shortcuts import render, redirect
# Create your views here.
from .service.forms import SignUpForm


def signup(request):
    if request.user.is_authenticated():
        return redirect('/')
    else:
        form = SignUpForm()

        return render(request, '../templates/account/signup.html', {form: form})


def signup_without_captcha(request):
    if request.user.is_authenticated():
        return redirect('/')
    else:
        form = SignUpForm()

        return render(request, '../templates/account/signup_without_captcha.html', {form: form})


def register(request):

    form = SignUpForm(request.POST)
    if form.save():
        messages.add_message(request, messages.SUCCESS, "Success")
        redirect('/index/')
    else:
        print form.errors.as_data()

    return render(request, 'account/signup.html', {'form': form})