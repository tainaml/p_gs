from django.core.management import BaseCommand
import csv
import re
import sys
from django.db import transaction
from apps.account.models import User
from apps.article.models import Article
from apps.core.business.article import save_feed_item
from apps.core.business.article import get_article

csv.field_size_limit(sys.maxsize)


url_pattern = re.compile(u'^http://www.portalgsti.com.br/(?P<year>\d+)/(?P<month>\d+)/(?P<slug>.+).html$')
date_pattern = re.compile(u'(?P<year>\d+)-(?P<month>\d+)-(?P<day>\d+)')

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

            author = User.objects.get(username='fernandopalma')
            row_count = 0
            for row in spamreader:
                regex_result = url_pattern.match(row[2])

                article_year = int(regex_result.group("year"))
                article_month = int(regex_result.group("month"))
                article_slug = regex_result.group("slug")

                # date_result = date_pattern.match(row[0])
                # date_year = int(date_result.group("year"))
                # date_month = int(date_result.group("month"))
                # date_day = date_result.group("day")

                article  = get_article(article_year, article_month, article_slug)['article']
                article_date = str(article_year) + "-" + (str(article_month) if  + article_month > 9 else "0" + str(article_month)) + "-" + "01 21:00:00.000000"
                if not article:

                    article = Article(
                        author=author,
                        createdin=article_date,
                        updatein=article_date,
                        publishin=article_date,
                        first_slug=article_slug,
                        title=row[1],
                        slug=article_slug,
                        text=row[3],
                        status=4
                    )
                    row_count+=1
                    article.save()
                    save_feed_item(article, {})

                else:
                    article.createdin=article_date
                    article.updatein=article_date
                    article.publishin=article_date
                    article.slug=article_slug
                    article.first_slug=article_slug
                    article.author=author
                    article.save()



