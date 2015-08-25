from django.core.mail import get_connection
from .backend import MailManageMessage


def send_email(to, subject, template=None, context={}, fail_silently=False, connection=None):
    '''

    :param to: string or tuple. Email recipient
    :param subject: string. Subject from email
    :param template: string. file with email template
    :param context: dict. Dictionary with context to template.
    :param fail_silently: boolean. If it is False, send_mail will raise an smtplib.SMTPException.
    :param connection: The optional email backend to use to send the mail
    :return: bool
    '''
    connection = connection or get_connection(fail_silently=fail_silently)
    mail = MailManageMessage(to, subject, template, context, connection=connection)
    return mail.send()