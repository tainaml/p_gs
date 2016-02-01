from apps.mailmanager import send_email
from celeryconfig import app

__author__ = 'ladeia'



@app.task
def send_mail_async(to, subject, template=None, context={}, fail_silently=False, connection=None):
    send_email(to, subject, template, context, fail_silently, connection)