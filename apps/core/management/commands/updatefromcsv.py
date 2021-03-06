from django.core.management import BaseCommand
import csv
import re
import sys
from apps.article.models import Article

csv.field_size_limit(sys.maxsize)


url_pattern = re.compile(u'^http://www.portalgsti.com.br/(?P<year>\d+)/(?P<month>\d+)/(?P<slug>.+).html$')
date_pattern = re.compile(u'(?P<year>\d+)-(?P<month>\d+)-(?P<day>\d+)')

class Command(BaseCommand):

    def add_arguments(self, parser):
        parser.add_argument('path', nargs='+', type=str)



    def handle(self, *args, **options):
        path =  options['path'][0]

        list_multiple= []
        list_doesnt_exist= []
        with open(path, 'r') as csvfile:
            spamreader = csv.reader(csvfile, delimiter='	')
            list_wrong_date = []

            for row in spamreader:
                regex_result = url_pattern.match(row[2])
                article_year = int(regex_result.group("year"))
                article_month = int(regex_result.group("month"))
                article_slug = regex_result.group("slug")

                date_result = date_pattern.match(row[0])
                date_year = int(date_result.group("year"))
                date_month = int(date_result.group("month"))
                date_day = date_result.group("day")

                if not (article_month==date_month and article_year==date_year):
                    list_wrong_date.append(row[2] + " > " + row[0])
                else:
                    try:
                        article = Article.objects.get(slug=article_slug, publishin__month=article_month, publishin__year=article_year)
                        article.text=row[3]
                        article.save()
                    except Article.DoesNotExist:
                        pass

