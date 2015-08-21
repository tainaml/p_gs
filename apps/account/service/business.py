from django.contrib.auth.hashers import make_password
from django.contrib.auth.models import User

__author__ = 'phillip'

def create_user(parameters=None):

    if not parameters:
        parameters = {}

    user = User()

    user.first_name = parameters['first_name']
    user.first_name = parameters['last_name']
    user.username = parameters['username']
    user.email = parameters['email']
    user.password = make_password(parameters['password'])

    user.save()
    return user if user.pk is not None else False



