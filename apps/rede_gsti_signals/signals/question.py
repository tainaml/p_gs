from django.conf import settings
from django.dispatch import receiver
from django.db.models.signals import post_save

from apps.question.models import Answer
from apps.notifications.service import business as Business
from apps.core.business import configuration


@receiver(post_save, sender=Answer)
def answer_question(sender, **kwargs):
    answer = kwargs.get('instance')
    created = kwargs.get('created')

    if answer and created:
        to = answer.question.author
        author = answer.author
        if to != author:
            if configuration.check_config_to_notify(to, settings.SOCIAL_COMMENT, answer.question):
                Business.send_notification(
                    author=author,
                    to=to,
                    notification_action=settings.SOCIAL_COMMENT,
                    target_object=answer.question
                )
