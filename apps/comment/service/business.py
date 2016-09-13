import logging

from django.contrib.contenttypes.models import ContentType
from django.conf import settings
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger

from ..models import Comment

__author__ = 'phillip'

logger = logging.getLogger('general')


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
    try:
        content_type = ContentType.objects.get_for_model(comment)
        children_comments = Comment.objects.filter(content_type=content_type, object_id=comment.id)
        for child_comment in children_comments:
            if comment:
                delete_comment(child_comment)
        comment.delete()
    except Exception, e:
        if settings.DEBUG:
            logger.error(e.message)
        return False
    return True


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


def get_content_object_by_content_type_and_id(content_type, object_id):
    content_type = ContentType.objects.get(model=content_type)
    return content_type.get_object_for_this_type(pk=object_id)


def get_comments_by_content_type_and_id(content_type=None, object_id=None, items_per_page=None, page=None):
    content_object = get_content_object_by_content_type_and_id(content_type, object_id)
    return get_comments_by_content_object(content_object, items_per_page, page)


def get_all_comments_by_content_object(content_object):
    comments = Comment.objects.filter(
        content_type=ContentType.objects.get_for_model(content_object),
        object_id=content_object.id
    )
    return comments

def get_comments_by_content_object(content_object=None, items_per_page=None, page=None):
    comments = get_all_comments_by_content_object(content_object).order_by("-creation_date")

    items_per_page = items_per_page if items_per_page else 10

    paginated_comments = Paginator(comments, items_per_page)

    try:
        paginated_comments = paginated_comments.page(page)
    except PageNotAnInteger:
        paginated_comments = paginated_comments.page(1)
    except EmptyPage:
        paginated_comments = []

    return paginated_comments


def count_comments_by_id_and_content_type(object_id, content_type):
    content_type = ContentType.objects.get(model=content_type)
    return Comment.objects.filter(object_id=object_id, content_type=content_type).count()
