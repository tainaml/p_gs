from django.contrib.auth.hashers import make_password
from django.contrib.auth.models import User

__author__ = 'phillip'


def create_user(parameters=None):

    """
    create_user method needs a array of parameters
    each parameter is named, a list of parameters are:
        first_name
        last_name
        username
        email
        password

    return: populated user if user are save ou False if has errors
    """
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



