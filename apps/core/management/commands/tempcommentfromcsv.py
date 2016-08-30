from django.core.management import BaseCommand
import csv
import re
import sys
from apps.article.models import Article
from apps.core.business.article import get_article

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
        count= []
        with open(path, 'r') as csvfile:
            spamreader = csv.reader(csvfile, delimiter='	')
            list_wrong_date = []

            for row in spamreader:
                regex_result = url_pattern.match(row[0])
                article_year = int(regex_result.group("year"))
                article_month = int(regex_result.group("month"))
                article_slug = regex_result.group("slug")


                article = get_article(article_year, article_month, article_slug)

                if not article['article']:
                    if row[0] not in count:
                        count.append(row[0])


                # print article['article'] if article['article'] else "Nao encontrado: %s" % row[0]

                # date_result = date_pattern.match(row[2])
                # date_year = int(date_result.group("year"))
                # date_month = int(date_result.group("month"))
                # date_day = date_result.group("day")
                #
                #
                #
                # print article_slug
        print count
