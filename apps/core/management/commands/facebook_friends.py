# coding=utf-8
from apps.account.models import User
from django.core.management import BaseCommand
from apps.core.tasks import notify_by_email_user_friends


class Command(BaseCommand):

    user_id = 23

    def add_arguments(self, parser):

        parser.add_argument('user_id', type=int)

    def handle(self, *args, **options):

        self.user_id = options.get('user_id', self.user_id)

        notify_by_email_user_friends.delay(self.user_id)
        print('Cabô')
