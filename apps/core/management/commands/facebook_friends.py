# coding=utf-8
import json
import urllib2
from apps.account.models import User
from django.core.management import BaseCommand
from apps.core.tasks import notify_by_email_user_friends


class Command(BaseCommand):

    user_id = 23

    def handle(self, *args, **options):

        user = User.objects.get(id=self.user_id)
        notify_by_email_user_friends.delay(user.id)
        print('Cabô')
