from django.db.models.signals import post_save
from django.dispatch import receiver

from apps.core.forms.configuration import ConfigNotificationsForm
from apps.userprofile.models import UserProfile


@receiver(post_save, sender=UserProfile)
def create_default_settings(sender, **kwargs):

    instance = kwargs.get('instance')
    created = kwargs.get('created')

    if not instance or not created:
        return

    form = ConfigNotificationsForm({
        'notify_follow': True,
        'notify_comment_article': True,
        'notify_comment_question': True,
        'notify_comment_comment': True,
        'notify_comment_answer': True,
        'notify_publications': 'all'
    })
    form.set_entity(instance.user)
    form.process()
