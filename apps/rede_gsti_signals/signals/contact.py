from django.conf import settings
from django.db.models.signals import post_save
from django.dispatch import receiver

from apps.contact.models import Contact
from apps.mailmanager import send_email


@receiver(post_save, sender=Contact)
def create_profile(sender, **kwargs):

    created = kwargs.get('created', False)

    if not created:
        return

    instance = kwargs.get('instance')

    if instance:
        email_subject = u"#{id}-{subject}".format(
            id=instance.id,
            subject=instance.subject.title if instance.subject else 'No subject'
        )
        send_email(
            to=str(settings.CONTACT_SEND_TO_EMAIL),
            subject=email_subject,
            template='mailmanager/contact.html',
            context={'contact': instance}
        )
