from __future__ import absolute_import
import os

from celery import Celery
from django.conf import settings


# set the default Django settings module for the 'celery' program.
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'rede_gsti.settings')
app = Celery('rede_gsti',  backend="rpc://", broker='amqp://localhost:5672')
app.conf.update(
    CELERY_TASK_SERIALIZER='json',
    CELERY_IGNORE_RESULT=False,
    )

CELERY_RESULT_BACKEND = 'rpc://'
CELERY_RESULT_PERSISTENT = False

# Using a string here means the worker will not have to
# pickle the object when using Windows.
app.config_from_object('django.conf:settings')
app.autodiscover_tasks(lambda: settings.INSTALLED_APPS)