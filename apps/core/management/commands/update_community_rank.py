from django.core.cache import caches
from django.core.management import BaseCommand
from apps.community.models import Community
from apps.gamification.models import update_rank_positions


class Command(BaseCommand):

    def handle(self, *args, **kwargs):
        communities = Community.objects.all()
        for community in communities:
            print "Updating rank for %s..." % community.slug
            update_rank_positions(community)