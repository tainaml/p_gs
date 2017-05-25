from django.core.management import BaseCommand
from push_notifications.models import GCMDevice


class Command(BaseCommand):

    def add_arguments(self, parser):
        parser.add_argument('title', nargs='+', type=str)
        parser.add_argument('message', nargs='+', type=str)
        parser.add_argument('registration_id', nargs='+', type=str)

    def handle(self, *args, **options):
        title =  options['title'][0]
        message =  options['message'][0]
        registration_id = options['registration_id'][0]

        device = GCMDevice.objects.get(registration_id=registration_id)

        response  = device.send_message(message, title=title, extra={"icon": "https://www.portalgsti.com.br/static/images/favicon-96x96.png"})
        print response


