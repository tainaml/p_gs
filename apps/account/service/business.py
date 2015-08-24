from django.contrib.auth.hashers import make_password
from django.contrib.auth.models import User
from django.core.mail import send_mail
from django.conf import settings

__author__ = 'phillip'

def create_user(parameters=None):

    if not parameters:
        parameters = {}

    user = User()

    user.first_name = parameters['first_name']
    user.last_name = parameters['last_name']
    user.username = parameters['username']
    user.email = parameters['email']
    user.password = make_password(parameters['password'])

    user.save()

    return user if user.pk is not None else False



def register_user(parameters=None):

    user = create_user(parameters)
    if user:
        #Todo -> move to settings file
        send_mail(
            subject='Assunto',
            message='Message',
            from_email=settings.DEFAULT_FROM_EMAIL,
            recipient_list=[user.email],
            fail_silently=False)

    return user
