#!/usr/bin/env python
# -*- coding: utf-8 -*-

from django.core.management import BaseCommand
import csv
import sys
from django.db import transaction
import re
from apps.account.models import User
from apps.core.business.article import get_article

csv.field_size_limit(sys.maxsize)

url_pattern = re.compile(u'^http://www.portalgsti.com.br/(?P<year>\d+)/(?P<month>\d+)/(?P<slug>.+).html$')

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

            main_user = User.objects.get(email='fernando.palma@gmail.com')

            for row in spamreader:
                regex_result = url_pattern.match(row[0])

                article_year = int(regex_result.group("year"))
                article_month = int(regex_result.group("month"))
                article_slug = regex_result.group("slug")

                article = get_article(article_year, article_month, article_slug)
                article= article['article']

                email = row[1].lower()

                if article:

                    article.author = main_user
                    try:
                        author = User.objects.get(email=email)
                        article.author=author
                        article.save()
                    except User.DoesNotExist:
                        pass

