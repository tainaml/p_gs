from celeryconfig import app

__author__ = 'ladeia'
from . import send_email


@app.task
def send_mail_async(to, subject, template=None, context={}, fail_silently=False, connection=None):
    send_email(to, subject, template, context, fail_silently, connection)