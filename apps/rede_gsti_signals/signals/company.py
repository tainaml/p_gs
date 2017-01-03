from django.conf import settings
from django.db.models.signals import post_save
from django.dispatch import receiver
from apps.company.models import Company


@receiver(post_save, sender=Company)
def company_updated(sender, **kwargs):
    instance = kwargs.get('instance', None)

    if instance and instance.user and instance.user.profile:
        profile = instance.user.profile
        profile.profile_picture = instance.logo
        profile.city = instance.city
        profile.city_hometown = instance.city
        profile.description = instance.description

        profile.save()

