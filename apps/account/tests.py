import hashlib
import random

from django.contrib.auth.models import User
from django.test import TestCase

from .models import MailValidation


class MailValidationTests(TestCase):

    def test_is_valid(self):

        user = User.objects.get(id=2)

        salt = hashlib.sha1(str(random.random())).hexdigest()[:5]
        activation_key = hashlib.sha1(salt+user.email).hexdigest()

        print activation_key

        token = MailValidation(token=activation_key, user=user)
        self.assertEqual(token.is_valid(), False)

