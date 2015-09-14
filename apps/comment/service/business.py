from django.contrib.contenttypes.models import ContentType
from django.conf import settings

__author__ = 'phillip'
from ..models import Comment


def create_comment(user=None, parameters=None):
    if not parameters:
        parameters = {}

    comment = Comment()
    comment.author = user
    content_type = ContentType.objects.get(model=parameters['content_type'])
    content_object = content_type.get_object_for_this_type(
        pk=parameters['content_object_id'])

    max_levels = settings.MAX_LEVELS if hasattr(settings,
                                                'MAX_LEVELS') else False

    comment.level = content_object.level + 1 if hasattr(content_object,
                                                        'level') else 1
    if max_levels is not False and comment.level > max_levels:
        comment.content_object = content_object.content_object
    else:
        comment.content_object = content_object

    comment.content = parameters['content']

    comment.save()

    return comment


def edit_comment(comment=None, parameters=None):
    comment.content = parameters['content']

    comment.save()

    return comment


def delete_comment(comment=None):
    content_type = ContentType.objects.get_for_model(comment)
    children_comments = Comment.objects.filter(content_type=content_type, object_id=comment.id)
    for child_comment in children_comments:
        if comment:
            delete_comment(child_comment)
    comment.delete()


def retrieve_comment(id):
    try:
        return Comment.objects.filter(pk=id)[0]
    except:
        return None


def retrieve_own_comment(comment_id=None, user=None):
    try:
        return Comment.objects.get(id=comment_id, author=user)
    except Comment.DoesNotExist:
        return None
