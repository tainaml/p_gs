from django.conf import settings
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.template.loader import render_to_string
from django.utils.html import strip_tags
from django.utils.safestring import mark_safe
import logging
from apps.core.business import configuration
from apps.notifications.models import Notification
from apps.mailmanager.tasks import send_mail_async


logger = logging.getLogger('signals')


@receiver(post_save, sender=Notification)
def try_dispatch_notification_mail(sender, **kwargs):

    instance = kwargs.get('instance')
    created = kwargs.get('created', False)

    if not instance or not created:
        print('Sem instancia {} ou nao criado {}'.format(bool(instance), bool(created)))
        return

    action_blacklist = instance.notification_action in getattr(settings, 'NOTIFICATION_MAIL_BLACKLIST', [])

    if configuration.check_config_to_notify(instance.to, 'mail_notification', None) and not action_blacklist:

        try:
            send_email_notification(instance.to, instance)
        except Exception as e:
            logger.error(e)
    else:
        print('Permissao negada')



def send_email_notification(to_obj, notification):
    if not to_obj.email:
        return

    notification_slug = settings.NOTIFICATION_ACTIONS.get(notification.notification_action)
    object_type = notification.target_content_type.name

    title_templates = [
        'notification/email/{}_{}/title.html'.format(notification_slug, object_type),
        'notification/email/{}/title.html'.format(notification_slug),
        'notification/email/title.html'
    ]

    content_templates = [
        'notification/email/{}_{}/content.html'.format(notification_slug, object_type),
        'notification/email/{}/content.html'.format(notification_slug),
        'notification/email/content.html'
    ]

    context = {
        'notification': notification,
        'notification_slug': notification_slug,
        'object_type': object_type,
    }

    mail_title = mark_safe(render_to_string(
        template_name=title_templates,
        context=context
    ))

    mail_content = render_to_string(
        template_name=content_templates,
        context=context
    )

    send_mail_async.delay(
        to=to_obj.email,
        subject=strip_tags(mail_title).strip(),
        template='mailmanager/notification.html',
        context={
            'mail_title': mail_title,
            'mail_content': mail_content,
        }
    )