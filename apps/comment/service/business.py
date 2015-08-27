from django.contrib.contenttypes.models import ContentType

__author__ = 'phillip'
from ..models import Comment

def create_comment(user=None, parameters=None):
    if not parameters:
        parameters = {}

    comment = Comment()
    comment.author = user
    content_type = ContentType.objects.get(model=parameters['content_type'])
    comment.content_object = content_type.get_object_for_this_type(pk=parameters['content_object_id'])
    comment.content = parameters['content']

    comment.save()