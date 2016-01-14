# -*- coding: utf-8 -*-

from django.test import TestCase

from apps.account.service.business import create_user

"""
For run tests do:
$ python manage.py test apps/account/tests/
"""

class TestAccountBusinessMethods(TestCase):

    def test_create_user(self):

        parameters = {}

        parameters['first_name'] = "André"
        parameters['last_name'] = "Nascimento"
        parameters['username'] = "andrenascimento"
        parameters['email'] = "andrenascimento@ideiaseo.com"
        parameters['password'] = "1234"
        parameters['is_active'] = False

        self.assertEqual(create_user(parameters).id, 1)