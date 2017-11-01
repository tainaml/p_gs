from apps.gamification.models import XP, NotAGamificationEntityException
from apps.socialactions.models import UserAction
from django.contrib.contenttypes.models import ContentType
from django.core.management import BaseCommand
from django.conf import settings


class Command(BaseCommand):

    def handle(self, *args, **options):


        actions = UserAction.objects.filter(action_type__in=[settings.SOCIAL_LIKE, settings.SOCIAL_UNLIKE, settings.SOCIAL_FOLLOW], content_type__in=ContentType.objects.filter(model__in=['article', 'question', 'answer', 'user']))
        index = 0
        print("Iniciando...")
        for action in actions:
            if index % 500 == 0:
                print("Processados: %s items" % str(index))
            try:
                XP.add_xp_for_action(action)
            except NotAGamificationEntityException:
                pass

            index+=1

        print("done")
