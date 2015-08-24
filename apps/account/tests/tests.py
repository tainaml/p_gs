# -*- coding: utf-8 -*-

from apps.account.service.business import create_user
from django.test import TestCase


class TestAccountBusinessMethods(TestCase):

    def test_create_user(self):

        parameters = {}

        parameters['first_name'] = "André"
        parameters['last_name'] = "Nascimento"
        parameters['username'] = "andrenascimento"
        parameters['email'] = "andrenascimento@ideiaseo.com"
        parameters['password'] = "1234"

        self.assertEqual(create_user(parameters).id, 1)