# coding=utf-8
import hashlib
import random
from apps.mailmanager.tasks import send_mail_async
from django.contrib.auth.hashers import make_password
from django.conf import settings
from django.contrib.auth import authenticate, login as auth_login, logout, update_session_auth_hash, get_user_model
from django.db import transaction
from django.utils import timezone
from django.utils.translation import ugettext as _
from apps.account.account_exceptions import AccountDoesNotExistException, TokenIsNoLongerValidException, \
    TokenIsNotActiveException, TokenDoesNotExistException

from ..models import TokenType
from apps.account.models import MailValidation, User

__author__ = 'phillip'

# UserModel = get_user_model()
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
    user.email = parameters['email'].lower()
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

        send_mail_async.delay(
            to=str(user.email),
            subject=_('Bem vindo!'),
            template='mailmanager/register_user.html',
            context={'user': user, 'token': token, 'base_url': settings.SITE_URL}
        )

    return user


def register_confirm(activation_key):

    """
    Method for confirm of user's account
    :param activation_key:
    :return user:
    """

    token = check_token_exist(activation_key)
    if token:
        if token.is_valid():
            user =  activate_account(token)
            if user:
                return token
            else:
                raise AccountDoesNotExistException()
        else:
            raise TokenIsNoLongerValidException()
    else:
        raise TokenDoesNotExistException()



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


def deactivate_account(request, user):

    try:
        user.is_active = False
        user.save(update_fields=['is_active'])
    except Exception, e:
        return False

    if not user.is_active:
        logout_user(request)

    return user


def create_token(user):

    """
    Method for create a new token
    :param user:
    :return: token
    """

    salt = hashlib.sha1(str(random.random())).hexdigest()[:5]
    activation_key = hashlib.sha1(salt+user.email).hexdigest()

    return activation_key


def register_token(user, token_type):

    """
    Method for register a new token

    :param user:
    :return: token object or False
    """

    activation_key = create_token(user)

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
    token.save(update_fields=['active'])

    return token


def authenticate_user(username_or_email=None, password=None):

    """ This method make a query in data base for username and password match
    :param username_or_email: Username or email to login
    :param password: password to authenticate
    :return:
    """
    user = authenticate(username=username_or_email, password=password)
    if not user:
        try:
            user = User.objects.get(email=username_or_email)
            if user:
                user = authenticate(username=user.username, password=password)
        except:
            user = False

    return user if user else False


def log_in_user(request=None, user=None):
    """ This method register an user as authenticated
    :param request: Request to include user into session
    :param user: user to attach
    :return:
    """
    UserModel = get_user_model()
    if user and user.usertype == UserModel.ORGANIZATION:
        return False
    try:
        auth_login(request, user)
        return True
    except:
        return False


def log_in_user_no_credentials(request, user):
    UserModel = get_user_model()
    if user.usertype == UserModel.ORGANIZATION:
        return

    from django.contrib.auth import load_backend, login
    if not hasattr(user, 'backend'):
        for backend in settings.AUTHENTICATION_BACKENDS:
            if user == load_backend(backend).get_user(user.pk):
                user.backend = backend
                break
    if hasattr(user, 'backend'):
        return login(request, user)


def logout_user(request=None):
    """ This method invalidate user session
    :param request: request to unlik user from session
    :return:
    """
    logout(request)


def update_password(request=None, user=None, new_password=None):
    """ This method update the user password
    :param user: User to update password
    :param new_password: new password to set
    :return: User
    """
    user.set_password(new_password)
    user.save()

    if request:
        update_session_auth_hash(request, user)

    return user


@transaction.atomic()
def forgot_password(user_email=None):
    try:
        user = User.objects.get(email=user_email)
        MailValidation.objects.filter(user=user, token_type=TokenType.RECOVERY_PASSWORD_CONFIRM).update(active=False)
        token = register_token(user=user, token_type=TokenType.RECOVERY_PASSWORD_CONFIRM)

        send_mail_async.delay(
            to=str(user.email),
            subject=_('Password Recovery'),
            template='mailmanager/password-recovery.html',
            context={'user': user, 'token': token, 'base_url': settings.SITE_URL}
        )

    except User.DoesNotExist:
        return False

    return token


@transaction.atomic()
def recovery_password(token=None, new_password=None):

    deactivate_token(token)
    update_password(user=token.user, new_password=new_password)
    return token


@transaction.atomic()
def resend_account_confirmation(user_email=None):
    try:
        user = User.objects.get(email=user_email)

        if not user.is_active:
            token = MailValidation.objects.filter(user=user, token_type=TokenType.REGISTER_ACCOUNT_CONFIRM, active=True).first()

            if not token or not token.is_valid():
                MailValidation.objects.filter(user=user, token_type=TokenType.REGISTER_ACCOUNT_CONFIRM).update(active=False)
                token = register_token(user=user, token_type=TokenType.REGISTER_ACCOUNT_CONFIRM)

            send_mail_async.delay(
                to=str(user.email),
                subject='Account Confirmation',
                template='mailmanager/resend-account-confirmation.html',
                context={'user': user, 'token': token, 'base_url': settings.SITE_URL}
            )
        else:
            return False

    except User.DoesNotExist:
        return False

    return token


def username_is_available(username=None):
    """
    Method checks if username is available
    :param username:
    :return True if username is available else False:
    """
    try:
        user = User.objects.get(username__iexact=username)
    except User.DoesNotExist:
        return True

    return False if user else True
