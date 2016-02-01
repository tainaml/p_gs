from django.core.mail import EmailMultiAlternatives
from django.template import Context
from django.template.loader import get_template
from django.utils.html import strip_tags
from django.core.mail.backends.smtp import EmailBackend


class MailManagedBackend(EmailBackend):
    '''
    Wrap Class to backend. Changes the django default backend class
    '''

    def __init(self, to, subject, template, context={}, *args, **kwargs):
        super(MailManagedBackend, self).__init__(to=to, subject=subject, *args, **kwargs)


class MailManageMessage(EmailMultiAlternatives):
    '''
    Custom Message Class. Receive template and context to render message
    '''

    def __init__(self, to, subject, template, context={}, connection=None):

        to = to if isinstance(to, (list, tuple)) else [to]

        self.template = template
        self.context = context

        super(MailManageMessage, self).__init__(
            to=to, subject=subject,
            connection=connection, from_email=None
        )

    def send(self, fail_silently=False):
        self.__render()
        return super(MailManageMessage, self).send(fail_silently)

    def __render(self):
        template = get_template(self.template)
        context = Context(self.context, autoescape=True)
        message = template.render(context)

        self.body = strip_tags(message)
        self.attach_alternative(message, 'text/html')