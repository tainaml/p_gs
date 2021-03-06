from __future__ import absolute_import
from celery import Celery
import os
from django.conf import settings


os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'rede_gsti.settings')
app = Celery('rede_gsti')

app.config_from_object('django.conf:settings')
app.autodiscover_tasks(lambda: settings.INSTALLED_APPS)


app.task(bind=True)
def debug_task(self):
    print('Request: {0!r}'.format(self.request))