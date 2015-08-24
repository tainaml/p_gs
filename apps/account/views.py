from django.contrib import messages
from django.shortcuts import render, redirect
# Create your views here.
from .service.forms import SignUpForm


def signup(request):
    if request.user.is_authenticated():
        return redirect('/')
    else:
        form = SignUpForm()
        render(request, '../templates/account/signup.html', {form: form})

    

    return 


def register(request):

    form = SignUpForm(request.POST)
    if form.save():
        messages.add_message(request, messages.SUCCESS, "Success")
        redirect('/index/')

    return render(request, 'account/signup.html', {'form': form})