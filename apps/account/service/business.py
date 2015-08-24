from django.contrib.auth.hashers import make_password
from django.contrib.auth.models import User
from django.core.mail import send_mail
from django.conf import settings

__author__ = 'phillip'


def create_user_by_parameters(parameters):
    user = User()
    user.first_name = parameters['first_name']
    user.last_name = parameters['last_name']
    user.username = parameters['username']
    user.email = parameters['email']
    user.password = make_password(parameters['password'])
    user.is_active = parameters['is_active']
    return user


def create_user(parameters=None):

    """
    Create_user method needs a array of parameters.
    Each parameter is named, a list of parameters are:
        first_name
        last_name
        username
        email
        password
        is_active

    return: populated user if user are save ou False if has errors
    """
    if not parameters:
        parameters = {}

    user = create_user_by_parameters(parameters)

    user.save()

    return user if user.pk is not None else False


def register_user(parameters=None):
    """
    Method for registar one user and send confirmation email link.

    """

    parameters['is_active'] = False
    user = create_user(parameters)
    if user and user.email:

        send_mail(
            subject='Assunto',
            message='Message',
            from_email=settings.DEFAULT_FROM_EMAIL,
            recipient_list=[user.email],
            fail_silently=False)

    return user
