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

