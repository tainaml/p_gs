__author__ = 'phillip'
from django.core.management import call_command, BaseCommand

class Command(BaseCommand):

    def handle(self, *args, **options):
        call_command("loaddata", "apps/core/fixtures/initial_data.json", ignorenonexistent=True)


