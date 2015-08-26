import hashlib
import random

from django.contrib.auth.hashers import make_password
from django.contrib.auth.models import User
from django.conf import settings
from django.contrib.auth import authenticate, login as auth_login, logout
from django.db import transaction
from django.utils import timezone
from ..models import TokenType
from apps.account.models import MailValidation
from apps.mailmanager import send_email

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

        token = register_token(user=user, token_type=TokenType.REGISTER_ACCOUNT_CONFIRM)
        send_email(
            to=str(user.email),
            subject='Bem vindo!',
            template='mailmanager/register_user.html',
            context={'user': user, 'token': token, 'base_url': settings.SITE_URL}
        )

    return user


def register_confirm(activation_key):

    """
    Method for confirm of user's account
    :param activation_key:
    :return:
    """

    token = check_token_exist(activation_key)
    if token and token.is_active() and token.is_valid():
        user = activate_account(token)
        if user:
            return True

    return False


@transaction.atomic
def activate_account(token):

    """
    Method for activate user account's

    :param token object:
    :return user object or False:
    """
    try:
        user = User.objects.get(id=token.user_id)
        user.is_active = True
        user.save()

        deactivate_token(token)

    except User.DoesNotExist:
        return False

    return user


def register_token(user, token_type):

    """
    Method for register a new token

    :param user:
    :return: token object or False
    """

    salt = hashlib.sha1(str(random.random())).hexdigest()[:5]
    activation_key = hashlib.sha1(salt+user.email).hexdigest()

    token = MailValidation(token=activation_key, user=user, link_date=timezone.now(), token_type=token_type)
    token.save()

    return token if token.pk is not None else False


def check_token_exist(activation_key):
    """
    Method checks if token exist
    :param activation_key:
    :return Token if exists else False:
    """
    try:
        token = MailValidation.objects.get(token=activation_key)
    except MailValidation.DoesNotExist:
        return False

    return token


def deactivate_token(token):

    token.active = False
    token.save()

    return token

def authenticate_user(username_or_email=None, password=None):
    user = authenticate(username=username_or_email, password=password)
    if not user:
        try:
            user = User.objects.get(email=username_or_email)
            if user:
                user = authenticate(username=user.username, password=password)
        except:
            user = False

    return user if user and user.is_active else False


def log_in_user(request=None, user=None):
    auth_login(request, user)


def logout_user(request=None):

    logout(request)


def update_password(user=None, new_password=None):
    user.set_password(new_password)
    user.save()

    return user


@transaction.atomic()
def forgot_password(user_email=None):
    try:
        user = User.objects.get(email=user_email)
        MailValidation.objects.filter(user=user, token_type=TokenType.RECOVERY_PASSWORD_CONFIRM).update(active=False)
        token = register_token(user=user, token_type=TokenType.RECOVERY_PASSWORD_CONFIRM)

        send_email(
            to=str(user.email),
            subject='Password Recovery',
            template='mailmanager/password-recovery.html',
            context={'user': user, 'token': token, 'base_url': settings.SITE_URL}
        )

    except User.DoesNotExist:
        return False

    return token

@transaction.atomic()
def recovery_password(token=None, new_password=None):

    deactivate_token(token)
    update_password(token.user, new_password)
    return token