from django.shortcuts import render
# Create your views here.
from .service.forms import SignUpForm


def index(request):

    form = SignUpForm()

    return render(request, '../templates/account/signup.html', {form: form})