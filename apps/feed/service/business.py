from django.contrib.contenttypes.models import ContentType
from ..models import FeedObject


def feed_get_or_create(content_instance):
    content_type = ContentType.objects.get_for_model(content_instance)

    feed_object, created = FeedObject.objects.get_or_create(
        content_type=content_type,
        object_id=content_instance.id
    )

    return feed_object