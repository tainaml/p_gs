from django.db.models.signals import post_save
from django.dispatch import receiver

from apps.account.models import User
from apps.core.business.account import save_profile

from functools import wraps


def disable_for_loaddata(signal_handler):
    """
    Decorator that turns off signal handlers when loading fixture data.
    """
    @wraps(signal_handler)
    def wrapper(*args, **kwargs):
        if kwargs['raw']:
            return
        signal_handler(*args, **kwargs)
    return wrapper


@receiver(post_save, sender=User)
@disable_for_loaddata
def create_profile(sender, **kwargs):

    instance = kwargs.get('instance')
    created = kwargs.get('created')

    if not created:
        return

    profile = save_profile(instance)
