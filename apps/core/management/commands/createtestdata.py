from django.core.management import BaseCommand, call_command

__author__ = 'phillip'


class Command(BaseCommand):

    def handle(self, *args, **options):
        call_command('dumpdata',

                     #User
                     'account.User',

                     # #Profile
                     'userprofile.UserProfile',

                     #Article
                     'article.Article',

                     #Question
                     'question.Question',
                     'question.Answer',

                    #FeedObject
                     'feed.FeedObject',

                     output='apps/core/fixtures/testdata.json')