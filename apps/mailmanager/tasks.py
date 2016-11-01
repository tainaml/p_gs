from apps.mailmanager import do_send_email
from rede_gsti.celery import app

__author__ = 'ladeia'


@app.task
def send_mail_async(to, subject, template=None, context=None, fail_silently=False, connection=None):
    return do_send_email(to, subject, template, context, fail_silently, connection)
