from django.core.mail import get_connection
from .backend import MailManageMessage


def send_email(to, subject, template=None, context={}, fail_silently=False, connection=None):
    connection = connection or get_connection(fail_silently=fail_silently)
    mail = MailManageMessage(to, subject, template, context, connection=connection)
    return mail.send()