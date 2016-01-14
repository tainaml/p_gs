from django.db.models.signals import post_save
from django.dispatch import receiver

from apps.article.models import Article
from apps.core.business.embeditem import EmbedBusiness


@receiver(post_save, sender=Article)
def article_action(sender, **kwargs):
    """

    Filter and save embed from articles

    :param sender: Signal required
    :param kwargs: Signal arguments
    :return: Embed Item (saved)
    """

    instance = kwargs['instance'] if 'instance' in kwargs else False
    if not instance:
        return

    embeds = EmbedBusiness(instance)
    embeds.save()