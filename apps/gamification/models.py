from __future__ import unicode_literals, absolute_import
from apps.article.models import Article
from apps.community.models import Community

from apps.geography.models import City
from apps.question.models import Question, Answer
from django.contrib.auth import get_user_model
from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType
from django.core.exceptions import ValidationError
from django.db.models import Sum
from django.utils import timezone
from django.utils.translation import ugettext as _
from django.db import models
from django.conf import settings
# Create your models here.


class NotAGamificationEntityException(Exception):
    pass

class XP():

    FOR_LIKE_ARTICLE_XP = 20
    FOR_LIKE_QUESTION_XP = 10
    FOR_LIKE_ANSWER_XP = 10
    FOR_DISLIKE_XP = -1
    FOR_FOLLOW = 50
    FOR_UNFOLLOW = -50

    @staticmethod
    def for_like(instance, communities):
        if type(instance) == Article:
            return int(XP.FOR_LIKE_ARTICLE_XP / len(communities))
        elif type(instance) == Question:
            return int(XP.FOR_LIKE_QUESTION_XP / len(communities))
        elif type(instance) == Answer:
            return int(XP.FOR_LIKE_ANSWER_XP / len(communities))
        else:
            raise NotAGamificationEntityException("Must be an article, question or answer")

    @staticmethod
    def for_dislike(instance, communities):
        if type(instance) not in [Article, Question, Answer]:
            raise NotAGamificationEntityException("Must be an article, question or answer")
        return XP.FOR_DISLIKE_XP * len(communities)

    @staticmethod
    def for_follow(instance):
        if type(instance) not in [get_user_model()]:
            raise NotAGamificationEntityException("Must be an article, question or answer")
        return XP.FOR_FOLLOW

    @staticmethod
    def for_unfollow(instance):
        if type(instance) not in [get_user_model()]:
            raise NotAGamificationEntityException("Must be an article, question or answer")
        return XP.FOR_UNFOLLOW



#User = get_user_model()
class TransactionType():
    CREDIT = 1
    DEBIT = 2

    @staticmethod
    def get_options():
        return [
            (TransactionType.CREDIT, "Credit"),
            (TransactionType.DEBIT, "Debit")
        ]

def limit_transaction_types(value):
    if value not in TransactionType.get_options():
        raise ValidationError(
            _('This is not a valid type'))

def limit_actions(value):
    if value not in settings.SOCIAL_LABELS.keys():
        raise ValidationError(
            _('This is not a valid action'))


class XPTransaction(models.Model):
    transaction_type = models.PositiveIntegerField(verbose_name="Transaction Type",
                                                   choices=TransactionType.get_options(), validators=[limit_transaction_types])
    action_type = models.PositiveIntegerField(verbose_name="Action type", choices=[(v, k) for k, v in settings.SOCIAL_LABELS.items()], validators=[limit_actions])
    value = models.PositiveIntegerField(verbose_name="Value")
    user = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='transactions')
    creation_date = models.DateTimeField(auto_now_add=timezone.now())
    city = models.ForeignKey(City, null=True, blank=True, related_name='transactions')
    by = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='transactions_related', null=True, blank=True)

    content_type = models.ForeignKey(ContentType)
    object_id = models.PositiveIntegerField()
    content_object = GenericForeignKey('content_type', 'object_id')

    communitiy = models.ForeignKey(to=Community, verbose_name=_("Community"), related_name="transactions", null=True, blank=True)

    def save_base(self, raw=False, force_insert=False,
                  force_update=False, using=None, update_fields=None):

        instance  = super(XPTransaction, self).save_base(raw=raw, force_insert=force_insert,
                  force_update=force_update, using=using, update_fields=update_fields)


        if instance.community:
            user_credits = XPTransaction.objects.filter(user=instance.user, community=instance.community,
                                                   transaction_type=TransactionType.CREDIT).annotate(credits=Sum("value"))
            debits = XPTransaction.objects.filter(user=instance.user, community=instance.community,
                                                   transaction_type=TransactionType.DEBIT).annotate(debits=Sum("value"))


            print user_credits
            print debits

            created, community_rank = CommunityRank.objects.get_or_create(
                user=instance.user,
                community=instance.community

            )
            community_rank.value = user_credits - debits




class CommunityRank(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='community_ranks')
    communitiy = models.ForeignKey(to=Community, verbose_name=_("Community"), related_name="rank")
    value = models.PositiveIntegerField(verbose_name="Value")

    class Meta:
        ordering = ['-value']


