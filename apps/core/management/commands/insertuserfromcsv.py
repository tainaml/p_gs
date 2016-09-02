#!/usr/bin/env python
# -*- coding: utf-8 -*-

from django.core.management import BaseCommand
import csv
import sys
from django.db import transaction
from apps.account.models import User

csv.field_size_limit(sys.maxsize)

class Command(BaseCommand):

    def add_arguments(self, parser):
        parser.add_argument('path', nargs='+', type=str)


    @transaction.atomic
    def handle(self, *args, **options):
        path =  options['path'][0]

        list_multiple= []
        list_doesnt_exist= []
        with open(path, 'r') as csvfile:
            spamreader = csv.reader(csvfile, delimiter='	')
            list_wrong_date = []

            for row in spamreader:
                full_name = row[0]
                full_name_list = full_name.split(" ")
                first_name = full_name_list[0].lower()
                last_name = ' '.join(full_name_list[1:]).lower()
                username = row[1].split("@")[0].lower()
                if username=='contato':
                    username = first_name+last_name.split(" ")[0]
                email = row[1].lower()
                password = 'pbkdf2_sha256$24000$YBcU98xl22lS$1FNq55MRTjKp4R6hr/ihrih3jOx63SQVqXkAqsXohdg='

                user  = User(
                    first_name=first_name,
                    last_name=last_name,
                    username=username,
                    email=email,
                    password=password
                )

                user.save()

