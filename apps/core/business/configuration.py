from django.contrib.contenttypes.models import ContentType
from django.db import transaction
from apps.configuration.models import ConfigKey, ConfigValues


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
        print e.message
        return False

    return configs_added, configs_updated