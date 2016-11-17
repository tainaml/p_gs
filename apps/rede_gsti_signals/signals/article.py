from django.db.models.signals import post_save
from django.dispatch import receiver
from apps.article.models import Article
from apps.core.tasks import clean_article_links


@receiver(post_save, sender=Article)
def clean_this_article(sender, **kwargs):

    instance = kwargs.get('instance')

    if not instance or instance.status != Article.STATUS_PUBLISH:
        return

    clean_article_links.delay(instance.id)


# @receiver(post_save, sender=Article)
# def article_action(sender, **kwargs):
#     """
#
#     Filter and save embed from articles
#
#     :param sender: Signal required
#     :param kwargs: Signal arguments
#     :return: Embed Item (saved)
#     """
#
#     # instance = kwargs['instance'] if 'instance' in kwargs else False
#     # if not instance:
#     #     return
#     #
#     # embeds = EmbedBusiness(instance)
#     # embeds.save()
#
#     pass