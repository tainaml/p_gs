from __future__ import absolute_import
from django.conf import settings

from django.core.mail import get_connection, send_mail
from apps.mailmanager.backend import MailManageMessage
from django.template import Context
from django.template.loader import get_template
from django.utils.html import strip_tags


def __render(template_path, context):
        template = get_template(template_path)
        context = Context(context, autoescape=True)
        message = template.render(context)
        return message

def do_send_email(to, subject, template=None, context=None, fail_silently=False, connection=None):
    message = __render(template, context=context)

    to = to if isinstance(to, (list, tuple)) else [to]

    return send_mail(
        subject=subject,
        html_message=message,
        message=strip_tags(message),
        from_email=getattr(settings, 'DEFAULT_FROM_EMAIL'),
        recipient_list=to
    )


def send_email(to, subject, template=None, context=None, fail_silently=False, connection=None):

    return do_send_email(to, subject, template, context, fail_silently, connection)
