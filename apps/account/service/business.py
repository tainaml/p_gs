from django.contrib.auth.hashers import make_password
from django.contrib.auth.models import User
from django.core.mail import send_mail
from django.conf import settings
from django.contrib.auth import authenticate, login as auth_login, logout

__author__ = 'phillip'


def create_user_by_parameters(parameters):

    """
    Method for create a User model Object populated with a dict of parameters.

    :param parameters: Dict of values, this key are(
        first_name
        last_name
        username
        email
        password
        is_active
    )
    :return: populated user
    """
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
    Method for get User Model Object and save him.

    :param parameters: Dict of values, this key are(
        first_name
        last_name
        username
        email
        password
        is_active
    )
    :return: populated user if user are save ou False if has errors
    """
    if not parameters:
        parameters = {}

    user = create_user_by_parameters(parameters)

    user.save()

    return user if user.pk is not None else False


def register_user(parameters=None):
    """
    Method for register user and send confirmation email link.
    :param parameters: Dict of values, this key are(
        first_name
        last_name
        username
        email
        password
    )
    :return: populated user if user are save ou False if has errors
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

def authenticate_user(username_or_email=None, password=None):
    user = authenticate(username=username_or_email, password=password)

    return user if user and user.is_active else False

def log_in_user(request=None, user=None):
    auth_login(request, user)

def logout_user(request=None):

    logout(request)

def update_password(user=None, new_password=None):
    user.set_password(new_password)
    user.save()

    return user

