from django.db.models.signals import post_save
from django.dispatch import receiver

from apps.account.models import User
from apps.core.business.account import save_profile


@receiver(post_save, sender=User)
def create_profile(sender, **kwargs):

    instance = kwargs.get('instance')
    created = kwargs.get('created')

    if not created:
        return

    profile = save_profile(instance)
