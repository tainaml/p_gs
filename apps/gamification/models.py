from __future__ import unicode_literals, absolute_import
from apps.article.models import Article
from apps.comment.models import Comment
from apps.community.models import Community
from apps.feed.models import ProfileStatus
from rede_gsti.celery import app

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
    FOR_DISLIKE_XP = 1
    FOR_FOLLOW = 50
    FOR_UNFOLLOW = -50

    @staticmethod
    def for_like(instance, communities):
        size_communities = len(communities) if len(communities) > 0 else 1
        if type(instance) == Article:

            return int(XP.FOR_LIKE_ARTICLE_XP / size_communities)
        elif type(instance) == Question:
            return int(XP.FOR_LIKE_QUESTION_XP / size_communities)
        elif type(instance) == Answer:
            return int(XP.FOR_LIKE_ANSWER_XP)
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
            raise NotAGamificationEntityException("Must be an user")
        return XP.FOR_FOLLOW

    @staticmethod
    def for_unfollow(instance):
        if type(instance) not in [get_user_model()]:
            raise NotAGamificationEntityException("Must be an user")
        return XP.FOR_UNFOLLOW

    @staticmethod
    def add_xp_for_action(action, reverse=False):

        value = None
        communities = None
        if action.action_type in [settings.SOCIAL_LIKE, settings.SOCIAL_UNLIKE, settings.SOCIAL_FOLLOW] and not isinstance(action.content_object, Comment) and not isinstance(action.content_object, ProfileStatus):

            if action.action_type == settings.SOCIAL_FOLLOW:
                communities = None
                user = action.content_object
            else:
                if isinstance(action.content_object, Answer):
                    communities = None
                elif not isinstance(action.content_object, Comment):
                    communities = action.content_object.feed.first().communities.all() if action.content_object else []

                user = action.content_object.author if action.content_object else None

            UserModel = get_user_model()
            if  user and type(user) == UserModel and user.gamification_member and user != action.author:


                transaction_type = None
                if  communities and len(communities) > 0:
                    if action.action_type == settings.SOCIAL_LIKE:
                        transaction_type = TransactionType.CREDIT if not reverse else TransactionType.DEBIT
                        value = XP.for_like(action.content_object, communities)
                    elif action.action_type == settings.SOCIAL_UNLIKE:
                        transaction_type = TransactionType.DEBIT if not reverse else TransactionType.CREDIT
                        value = XP.for_dislike(action.content_object, communities)
                elif action.action_type == settings.SOCIAL_FOLLOW:
                    transaction_type = TransactionType.CREDIT if not reverse else TransactionType.DEBIT
                    value = XP.for_follow(action.content_object)

                try:
                    city = user.profile.city
                except Exception:
                    city = None



                if communities:
                    communities_count = communities.count()
                    for community in communities:

                        transaction = XPTransaction(
                            transaction_type=transaction_type,
                            action_type=action.action_type,
                            value=value/communities_count if communities_count != 0 else value,
                            user=user,
                            city= city,
                            by=action.author,
                            content_type=action.content_type,
                            object_id=action.object_id,
                            community=community

                        )
                        transaction.save()
                else:
                    transaction = XPTransaction(
                            transaction_type=transaction_type,
                            action_type=action.action_type,
                            value=value,
                            user=user,
                            city= city,
                            by=action.author,
                            content_type=action.content_type,
                            object_id=action.object_id,
                            community=None

                        )
                    transaction.save()

                user_credits = XPTransaction.objects.filter(user=user,
                                               transaction_type=TransactionType.CREDIT).aggregate(credits=Sum("value"))
                debits = XPTransaction.objects.filter(user=user,
                                                                   transaction_type=TransactionType.DEBIT).aggregate(debits=Sum("value"))
                user_value = (user_credits['credits'] or 0) - (debits['debits'] or 0)

                user.xp = user_value
                user.save()




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

    community = models.ForeignKey(to=Community, verbose_name=_("Community"), related_name="transactions", null=True, blank=True)



    def save(self, force_insert=False, force_update=False, using=None,
             update_fields=None):


        super(XPTransaction, self).save(force_insert=force_insert,
                  force_update=force_update, using=using, update_fields=update_fields)




        if self.community:
            update_rank.delay(self.user, self.community)


class CommunityRank(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='community_ranks')
    community = models.ForeignKey(to=Community, verbose_name=_("Community"), related_name="rank")
    value = models.BigIntegerField(verbose_name="Value", null=True, blank=True)
    rank_position = models.PositiveIntegerField(verbose_name="Position", default=0)

    class Meta:
        ordering = ['-value']


@app.task
def update_rank(user, community):
    if community:

        user_credits = XPTransaction.objects.filter(user=user, community=community,
                                               transaction_type=TransactionType.CREDIT).aggregate(credits=Sum("value"))
        debits = XPTransaction.objects.filter(user=user, community=community,
                                               transaction_type=TransactionType.DEBIT).aggregate(debits=Sum("value"))


        community_rank, created = CommunityRank.objects.get_or_create(
            user=user,
            community=community

        )

        community_rank.value = (user_credits['credits'] or 0) - (debits['debits'] or 0)
        community_rank.save()
        update_rank_positions.delay(community)


@app.task
def update_rank_positions(community):
    community_rank_list = CommunityRank.objects.filter(community=community).order_by("-value")

    rank_position = 1
    for community_rank in community_rank_list:
        community_rank.rank_position = rank_position
        community_rank.save()
        rank_position+= 1


