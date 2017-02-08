#!/usr/bin/env python
# -*- coding: utf-8 -*-

from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver
from apps.comment.models import Comment
from apps.core.business.content_types import ContentTypeCached


def __get_comment_count(content_object):
    content_type = ContentTypeCached.objects.get_for_model(content_object)
    return Comment.objects.filter(
                    content_type=content_type,
                    object_id=content_object.id
                ).count()


def change_comment_count(instance):
    comment_count = __get_comment_count(instance.content_object)
    instance.content_object.comment_count = comment_count
    instance.content_object.save()


@receiver(post_delete, sender=Comment)
def comment_count_action(sender, **kwargs):
    instance = kwargs['instance'] if 'instance' in kwargs else False
    if not instance:
        return
    change_comment_count(instance)

@receiver(post_save, sender=Comment)
def comment_count_action(sender, **kwargs):
    """

    Change comment count for content object

    :param sender: Signal required
    :param kwargs: Signal arguments
    :return: Embed Item (saved)
    """

    instance = kwargs['instance'] if 'instance' in kwargs else False
    if not instance:
        return

    change_comment_count(instance)

