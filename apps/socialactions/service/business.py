from django.contrib.auth.models import User
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from django.db.models import Q
from apps.article.models import Article
from apps.taxonomy.models import Taxonomy
from apps.taxonomy.service.business import get_related_list_top_down

from ..models import UserAction, Counter, UserActionCounter
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


def get_user_by_params(params=None):
    try:
        user_action = UserAction.objects.filter(**params)[0]
    except UserAction.DoesNotExist:
        user_action = None

    return user_action


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
    return user_acted_by_content_and_object_id(user, content_type, object_id, 'like')


def user_liked_by_object(user=None, content_object=None):
    return user_acted_by_object(user, content_object, 'like')


def user_unliked_by_id_and_content_type(user=None, content_type=None, object_id=None):
    return user_acted_by_content_and_object_id(user, content_type, object_id, 'unlike')


def user_unliked_by_object(user=None, content_object=None):
    return user_acted_by_object(user, content_object, 'unlike')


def user_followed(user=None, content_type=None, object_id=None):
    return user_acted_by_content_and_object_id(user, content_type, 'follow', object_id)


def user_likes_by_object(user=None, content_object=None):
    return user_count_acted_by_object(user, content_object, 'like')


def user_likes_by_object_content_type_and_id(user=None, content_type=None, object_id=None):
    return user_count_acted_by_content_and_id(user, content_type, object_id, 'like')


def user_unlikes_by_object(user=None, content_object=None):
    return user_count_acted_by_object(user, content_object, 'unlike')


def user_unlikes_by_object_content_type_and_id(user=None, content_type=None, object_id=None):
    return user_count_acted_by_content_and_id(user, content_type, object_id, 'unlike')


def followers_count(user=None, content_object=None):
    return user_count_acted_by_object(user, content_object, 'follow')


def followings_count(author=None, content_type=None):
    content_type = ContentType.objects.get(model=content_type)
    action_type = get_by_label("follow")

    user_action_count = UserAction.objects.filter(author=author,
                                                  content_type=content_type,
                                                  action_type=action_type).count()

    return user_action_count


# Action methods

def suggest_post(author, object_to_link, content, to_user):

    to_users = to_user.split(',')

    suggested_to = []

    article = Article.objects.get(id=object_to_link)
    if not article:
        raise Exception('Article is not exists!')

    content_type = ContentType.objects.get_for_model(article)

    try:

        for id_user in to_users:
            user = User.objects.get(id=id_user)

            if user:
                user_action, created = UserAction.objects.get_or_create(
                    author=author,
                    content_type=content_type,
                    object_id=article.id,
                    action_type=settings.SOCIAL_SUGGEST,
                    target_user=user
                )
                suggested_to.append(user)
    except:
        raise Exception('Error!')

    return True


def act_by_content_type_and_id(user=None, content_type=None, object_id=None, action_type=None):

    action_type_key = get_by_label(action_type)

    inverse_action_list = settings.SOCIAL_INVERSE_ACTIONS[action_type_key] \
        if action_type_key in settings.SOCIAL_INVERSE_ACTIONS.keys() else []
    user_acted = user_acted_by_content_and_object_id(user, content_type, object_id, action_type)

    if user_acted and user_acted.action_type == action_type_key:
        user_acted.delete()

        return


    for inverse_action in inverse_action_list:
        if action_type_key != inverse_action:
            inverse_action_user = user_acted_by_content_and_object_id_and_action_id(user, content_type, object_id,
                                                                                    inverse_action)
            if inverse_action_user is not False:
                inverse_action_user.delete()

    if content_type in settings.SOCIAL_ENTITIES[action_type_key]:
        action = UserAction(
            author=user,
            action_type=action_type_key,
            content_object=get_content_object(content_type, object_id)
        )

        action.save()

        return action
    else:

        raise NotFoundSocialSettings("not_found_setting_exception",
                                     "Entity %s not found in SOCIAL_ENTITIES" % action_type_key)


def get_users_ids_acted_by_model_and_action(model=None, action=None, user=None):
    content_type = ContentType.objects.get_for_model(user)

    users_ids = []
    users_actions = UserAction.objects.filter(
        content_type=content_type,
        action_type=action,
        author=user
    ).prefetch_related("author")

    for user in users_actions:
        users_ids.append(user.object_id)

    return users_ids


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
        # list = list.page(list.num_pages)
        list = []

    return list


def get_users_acted_by_author(author=None, action=None, content_type=None, filter_parameters=None, items_per_page=None,
                              page=None):
    if not filter_parameters:
        filter_parameters = {}

    content_type = get_model_type(content_type)
    parameters = filter_parameters.copy()
    parameters['content_type'] = content_type
    parameters['author'] = author.id
    parameters['action_type'] = action

    users_actions = UserAction.objects.filter(**parameters).prefetch_related("author", "content_object")

    if items_per_page is not None and page is not None:
        list_users = Paginator(users_actions, items_per_page)
        try:
            list_users = list_users.page(page)
        except PageNotAnInteger:
            list_users = list_users.page(1)
        except EmptyPage:
            list_users = []
    else:
        list_users = users_actions

    return list_users


def get_random_users_acted_by_author(author=None, action=None, content_type=None, filter_parameters=None,
                                     items_per_page=None, page=None):
    if not filter_parameters:
        filter_parameters = {}

    content_type = get_model_type(content_type)
    parameters = filter_parameters.copy()
    parameters['content_type'] = content_type
    parameters['author'] = author.id
    parameters['action_type'] = action

    users_actions = UserAction.objects.filter(**parameters).order_by('?').prefetch_related('author')

    if items_per_page is not None and page is not None:
        list_users = Paginator(users_actions, items_per_page)
        try:
            list_users = list_users.page(page)
        except PageNotAnInteger:
            list_users = list_users.page(1)
        except EmptyPage:
            list_users = []
    else:
        list_users = users_actions

    return list_users


def get_users_acted_by_author_with_parameters(author=None, action=None, content_type=None,
                                              criteria=None, category=None, items_per_page=None, page=None):
    content_type = get_model_type(content_type)

    if category:
        # category = Taxonomy.objects.get(pk=category)
        categories = get_related_list_top_down([category])
    else:
        categories = []

    condition = (
        Q(content_type=content_type) &
        Q(author=author) &
        Q(action_type=action)
    )

    if criteria:
        condition &= Q(community__title__icontains=criteria)

    if category and categories:
        condition &= Q(community__taxonomy__in=categories)

    users_actions = UserAction.objects.filter(condition).prefetch_related('author')

    if items_per_page is not None and page is not None:
        list_users = Paginator(users_actions, items_per_page)
        try:
            list_users = list_users.page(page)
        except PageNotAnInteger:
            list_users = list_users.page(1)
        except EmptyPage:
            list_users = []
    else:
        list_users = users_actions

    return list_users


def count_actions_by_user_and_action(user=None, action=None, **filters):

    try:
        count = UserActionCounter.objects.get(author=user,
            action_type=get_by_label(action), **filters).count
    except UserActionCounter.DoesNotExist:
        count = 0

    return count
