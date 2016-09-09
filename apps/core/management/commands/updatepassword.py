from django.core.management import BaseCommand
import csv
import re
import sys
from apps.account.models import User

csv.field_size_limit(sys.maxsize)

class Command(BaseCommand):

    def add_arguments(self, parser):
        parser.add_argument('password', nargs='+', type=str)
        parser.add_argument('path', nargs='+', type=str)



    def handle(self, *args, **options):
        path =  options['path'][0]
        password =  options['password'][0]

        list_multiple= []
        list_doesnt_exist= []
        with open(path, 'r') as csvfile:
            spamreader = csv.reader(csvfile, delimiter='	')
            list_wrong_date = []

            for row in spamreader:
                full_name =  row[0]
                email =  row[1]


                try:
                    user = User.objects.get(email=email)
                    user.set_password(password)
                    user.save()
                except User.DoesNotExist:
                    print "Email %s doesn't exists" % email


