import logging

from django.contrib.contenttypes.models import ContentType
from django.db import transaction
from django.db.models import Q

from apps.configuration.models import ConfigKey, ConfigValues, ConfigGroup
from apps.core.business.content_types import ContentTypeCached
from rede_gsti import settings

logger = logging.getLogger('general')


def get_system_configs(config_group=None, show=True):
    if not show:
        show = True

    try:
        criteria = Q(show=show)

        if config_group:
            group = ConfigGroup.objects.get(group=config_group)
            criteria &= Q(group=group)

        config_keys = ConfigKey.objects.filter(criteria).order_by('order')
    except Exception as e:
        if settings.DEBUG:
            logger.error(e.message)
        config_keys = []

    return config_keys


def get_configs(entity, config_group=None):
    content_type = ContentTypeCached.objects.get_for_model(entity)

    try:
        criteria = Q(content_type=content_type) & Q(object_id=entity.id)

        if config_group:
            group = ConfigGroup.objects.get(group=config_group)
            key = ConfigKey.objects.filter(group=group)
            criteria &= Q(key__in=key)

        configs = ConfigValues.objects.filter(criteria)

    except Exception as e:
        if settings.DEBUG:
            logger.error(e.message)
        configs = None

    return configs


@transaction.atomic()
def save_configs(entity, data):

    content_type = ContentTypeCached.objects.get_for_model(entity)

    configs_created = []
    configs_updated = []

    try:
        for key, value in data.items():
            config, created = ConfigValues.objects.get_or_create(
                key=ConfigKey.objects.get(key=key),
                content_type=content_type,
                object_id=entity.id
            )

            if config.value != value:
                config.value = value
                config.save()

            if created:
                configs_created.append(config)
            else:
                configs_updated.append(config)

    except Exception as e:
        if settings.DEBUG:
            logger.error(e.message)
        return False

    return configs_created, configs_updated


def check_config_to_notify(to_user, action, target_object=None):

    key_prefix = 'notify_'

    allowed_social_tags = [
        settings.SOCIAL_COMMENT,
        settings.NOTIFICATION_SUGGEST
    ]

    if action in allowed_social_tags and target_object:
        key_slug = key_prefix + settings.SOCIAL_LABELS[action] + '_'
        target_content = ContentTypeCached.objects.get_for_model(model=target_object)
        key_slug += target_content.model

    elif action in ['mail_notification']:
        key_slug = "{}{}".format(key_prefix, action)

    elif action in settings.SOCIAL_LABELS:
        key_slug = key_prefix
        key_slug += settings.SOCIAL_LABELS[action]

    elif action in settings.NOTIFICATION_ACTIONS:
        key_slug = key_prefix
        key_slug += settings.NOTIFICATION_ACTIONS[action]

    else:
        return False


    try:

        config, created = ConfigValues.objects.get_or_create(
            object_id=to_user.id,
            content_type=ContentTypeCached.objects.get_for_model(to_user),
            key=ConfigKey.objects.get(key=key_slug)
        )
        if created:
            config.value = str(True)
            config.save()
    except Exception as e:
        if settings.DEBUG:
            logger.error(e.message)
        if key_slug in ['notify_mail_notification', 'notify_useralert']:
            return True
        return False

    if config.value == "True":
        return True
    elif config.value == "False":
        return False
    else:
        return config.value
