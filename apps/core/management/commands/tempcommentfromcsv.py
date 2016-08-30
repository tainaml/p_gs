from django.core.management import BaseCommand
import csv
import re
import sys
from apps.article.models import Article
from apps.core.business.article import get_article
from apps.temp_comment.models import TempComment

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

            for row in spamreader:
                regex_result = url_pattern.match(row[0])
                article_year = int(regex_result.group("year"))
                article_month = int(regex_result.group("month"))
                article_slug = regex_result.group("slug")

                article = get_article(article_year, article_month, article_slug)
                article= article['article']

                if article:

                    comment_id = row[1]
                    answer_id = row[2]
                    author = row[4]
                    date = row[3]
                    text = row[5]

                    if answer_id:
                        temp_comment =TempComment(
                            author=author,
                            google_id=comment_id,
                            parent_google_id=answer_id,
                            creation_date=date,
                            text=text
                        )

                    else:
                        temp_comment =TempComment(
                            author=author,
                            google_id=comment_id,
                            parent_google_id=answer_id,
                            creation_date=date,
                            text=text,
                            article=article
                        )

                    temp_comment.save()





