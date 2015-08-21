from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User


def sign_up(request):
    if request.user.is_authenticated():
        return HttpResponseRedirect('/')
    else:
        return render(request, 'account/signup.html')


def register(request):
    username = request.POST['username']
    first_name = request.POST['first_name']
    last_name = request.POST['last_name']
    email = request.POST['email']
    password = request.POST['password']
    password2 = request.POST['confirm_password']

    try:
        user = User.objects.get(email=email)
        return render(request, 'account/signup.html', {'error_message': ("USER_ALREADY_EXISTS")})
    except:
        if password == password2:
            user = User.objects.create_user(username=username, first_name=first_name, last_name=last_name, email=email, password=password)
            user.is_active = True
            user.save()

            return render(request, 'account/signin.html', {'error_message': ("REGISTERED_SUCCESSFULLY")})
        else:
            return render(request, 'account/signup.html', {'error_message': ("PASSWORD_DO_NOT_MATCH")})