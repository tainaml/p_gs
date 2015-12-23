from django.core.cache import caches
from django.core.management import BaseCommand

class Command(BaseCommand):

    def handle(self, *args, **kwargs):
        cache = caches['default']
        cache.clear()
        self.stdout.write('Cleared Cache\n')