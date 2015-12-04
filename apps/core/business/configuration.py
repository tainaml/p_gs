from django.contrib.contenttypes.models import ContentType
from django.db import transaction
from django.db.models import Q
from apps.configuration.models import ConfigKey, ConfigValues, ConfigGroup


def get_configs(entity, config_group=None):

    content_type = ContentType.objects.get_for_model(entity)

    try:
        criteria = Q(content_type=content_type) & Q(object_id=entity.id)

        if config_group:
            group=ConfigGroup.objects.get(group=config_group)
            key = ConfigKey.objects.filter(group=group)

            criteria &= Q(key=key)

        configs = ConfigValues.objects.filter(criteria)

    except Exception, e:
        configs = None

    return configs


@transaction.atomic()
def save_configs(entity, data):

    content_type = ContentType.objects.get_for_model(entity)

    configs_added = []
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
                configs_added.append(config)
            else:
                configs_updated.append(config)

    except Exception, e:
        return False

    return configs_added, configs_updated