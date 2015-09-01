__author__ = 'phillip'
from ..models import UserAction
from ..app_settings import settings as social_settings

from django.contrib.contenttypes.models import ContentType

# Meta methods

def get_by_label(str_label=None):
    for label in social_settings.LABELS.keys():
        if str_label and social_settings.LABELS[label].lower()== str_label.lower():
            return label

    return None

def get_content_by_object(content_object=None):
    return ContentType.objects.get_for_model(content_object)


def get_model_type(content_type=None):
    model_type = ContentType.objects.get(model=content_type)

    return model_type

def get_content_object(content_type=None, object_id=None):
    content_type = get_model_type(content_type)
    content_object = content_type.get_object_for_this_type(pk=object_id)

    return content_object



def user_acted_by_object(user=None, content_object=None, action_type=None):
    content_type = ContentType.objects.get_for_model(content_object)
    try:
        user_action = UserAction.objects.filter(content_type=content_type,
                                            author=user,
                                            object_id=content_object.id,
                                            action_type=get_by_label(action_type))[0]
    except:
        user_action = False

    return user_action

def user_count_acted_by_object(user=None, content_object=None, action_type=None):
    content_type = ContentType.objects.get_for_model(content_object)

    user_action_count = UserAction.objects.filter(content_type=content_type,
                                            author=user,
                                            object_id=content_object.id,
                                            action_type=get_by_label(action_type)).count()

    return user_action_count



def user_acted_by_content_and_id(user=None, content_type=None,
                                 object_id=None, action_type=None):
    content_object = get_content_object(content_type, object_id)

    return user_acted_by_object(user, content_object, action_type)

def user_count_acted_by_content_and_id(user=None, content_type=None,
                                       object_id=None, action_type=None):
    content_object = get_content_object(content_type, object_id)

    return user_count_acted_by_object(user, content_object, action_type)


# Specialization methods

def user_liked_by_id_and_content_type(user=None, content_type=None, object_id=None):
    return user_acted_by_content_and_id(user, content_type, 'like', object_id)


def user_liked_by_object(user=None, content_object=None):
    return user_acted_by_object(user,content_object, 'like')


def user_unliked_by_id_and_content_type(user=None, content_type=None, object_id=None):
    return user_acted_by_content_and_id(user, content_type, 'unlike', object_id)

def user_unliked_by_object(user=None, content_object=None):
    return user_acted_by_object(user,content_object, 'unlike')


def user_followed(user=None, content_type=None, object_id=None):
    return user_acted_by_content_and_id(user, content_type, 'follow', object_id)


def user_likes_by_object(user=None, content_object=None):

    return user_count_acted_by_object(user,content_object, 'like')

def user_likes_by_object_content_type_and_id(user=None, content_type=None, object_id=None):

    return user_count_acted_by_content_and_id(user,content_type, object_id, 'like')

def user_unlikes_by_object(user=None, content_object=None):

    return user_count_acted_by_object(user,content_object, 'unlike')

def user_unlikes_by_object_content_type_and_id(user=None, content_type=None, object_id=None):

    return user_count_acted_by_content_and_id(user,content_type, object_id, 'unlike')

# Action methods

def act_by_action_and_object(user=None, action_type=None, content_object=None):
    pass