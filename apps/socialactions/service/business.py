from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage

__author__ = 'phillip'
from ..models import UserAction
from django.conf import settings
from ..localexceptions import NotFoundSocialSettings
from django.contrib.contenttypes.models import ContentType

# Meta methods

def get_by_label(str_label=None):
    if hasattr(settings, 'SOCIAL_LABELS'):
        for label in settings.SOCIAL_LABELS.keys():
            if str_label and settings.SOCIAL_LABELS[label].lower() == str_label.lower():
                return label
    else:
        NotFoundSocialSettings("not_found_setting_exception", "SOCIAL_LABELS must be declared")

    raise NotFoundSocialSettings("not_found_setting_exception", "SOCIAL_LABELS - {s%}" % str_label)


def get_content_by_object(content_object=None):
    return ContentType.objects.get_for_model(content_object)


def get_model_type(content_type=None):
    model_type = ContentType.objects.get(model=content_type)

    return model_type


def get_content_object(content_type=None, object_id=None):
    content_type = get_model_type(content_type)
    content_object = content_type.get_object_for_this_type(pk=object_id)

    return content_object


def user_acted_by_object_and_action_id(user=None, content_object=None, action_type_id=None):
    content_type = ContentType.objects.get_for_model(content_object)
    try:
        user_action = UserAction.objects.filter(content_type=content_type,
                                            author=user,
                                            object_id=content_object.id,
                                            action_type=action_type_id)[0]
    except:
        user_action = False

    return user_action


def user_acted_by_object(user=None, content_object=None, action_type=None):
    return user_acted_by_object_and_action_id(user, content_object, get_by_label(action_type))


def user_count_acted_by_object_and_action_id(user=None, content_object=None, action_type=None):
    content_type = ContentType.objects.get_for_model(content_object)

    user_action_count = UserAction.objects.filter(content_type=content_type,
                                                  object_id=content_object.id,
                                                  action_type=action_type).count()

    return user_action_count


def user_count_acted_by_object(user=None, content_object=None, action_type=None):
    return user_count_acted_by_object_and_action_id(user, content_object, get_by_label(action_type))


def user_acted_by_content_and_object_id(user=None, content_type=None,
                                        object_id=None, action_type=None):
    content_object = get_content_object(content_type, object_id)

    return user_acted_by_object(user, content_object, action_type)


def user_acted_by_content_and_object_id_and_action_id(user=None, content_type=None,
                                                      object_id=None, action_type=None):
    content_object = get_content_object(content_type, object_id)

    return user_acted_by_object_and_action_id(user, content_object, action_type)


def user_count_acted_by_content_and_id(user=None, content_type=None,
                                       object_id=None, action_type=None):
    content_object = get_content_object(content_type, object_id)

    return user_count_acted_by_object(user, content_object, action_type)


# Specialization methods

def user_liked_by_id_and_content_type(user=None, content_type=None, object_id=None):
    return user_acted_by_content_and_object_id(user, content_type, 'like', object_id)


def user_liked_by_object(user=None, content_object=None):
    return user_acted_by_object(user,content_object, 'like')


def user_unliked_by_id_and_content_type(user=None, content_type=None, object_id=None):
    return user_acted_by_content_and_object_id(user, content_type, 'unlike', object_id)


def user_unliked_by_object(user=None, content_object=None):
    return user_acted_by_object(user,content_object, 'unlike')


def user_followed(user=None, content_type=None, object_id=None):
    return user_acted_by_content_and_object_id(user, content_type, 'follow', object_id)


def user_likes_by_object(user=None, content_object=None):

    return user_count_acted_by_object(user,content_object, 'like')


def user_likes_by_object_content_type_and_id(user=None, content_type=None, object_id=None):

    return user_count_acted_by_content_and_id(user,content_type, object_id, 'like')


def user_unlikes_by_object(user=None, content_object=None):

    return user_count_acted_by_object(user,content_object, 'unlike')


def user_unlikes_by_object_content_type_and_id(user=None, content_type=None, object_id=None):

    return user_count_acted_by_content_and_id(user,content_type, object_id, 'unlike')

# Action methods


def act_by_content_type_and_id(user=None, content_type=None, object_id=None, action_type=None):
    action_type_key = get_by_label(action_type)
    inverse_action_list = settings.SOCIAL_INVERSE_ACTIONS[action_type_key]
    user_acted = user_acted_by_content_and_object_id(user, content_type, object_id, action_type)

    if user_acted and user_acted.action_type == action_type_key:
        user_acted.delete()
        return

    for inverse_action in inverse_action_list:
        if action_type_key != inverse_action:
            inverse_action_user = user_acted_by_content_and_object_id_and_action_id(user, content_type, object_id, inverse_action)
            if inverse_action_user is not False:
                inverse_action_user.delete()


    if content_type in settings.SOCIAL_ENTITIES[action_type_key]:
        action = UserAction(
            author=user,
            action_type=action_type_key,
            content_object=get_content_object(content_type, object_id)
        )

        action.save()
    else:
        raise NotFoundSocialSettings("not_found_setting_exception", "Entity %s not found in SOCIAL_ENTITIES" % action_type_key)



def get_users_acted_by_model(model=None, action=None, filter_parameters=None,
                             itens_per_page=None, page=None):

    if not filter_parameters:
        filter_parameters = {}

    content_type = ContentType.objects.get_for_model(model)
    parameters = filter_parameters.copy()
    parameters['content_type'] = content_type
    parameters['object_id'] = model.id
    parameters['action_type'] = action

    users_actions = UserAction.objects.filter(**parameters).prefetch_related('author')

    list = Paginator(users_actions, itens_per_page)
    try:
        list = list.page(page)
    except PageNotAnInteger:
        # If page is not an integer, deliver first page.
        list = list.page(1)
    except EmptyPage:
        # If page is out of range (e.g. 9999), deliver last page of results.
        list = list.page(list.num_pages)

    return list




