from django.contrib.contenttypes.models import ContentType
from apps.core.business.content_types import ContentTypeCached

from ..models import FeedObject


def get_feed(content_instance):

    try:
        return content_instance.feed if content_instance.feed else content_instance.feed.first()
    except Exception:
        pass

    content_type = ContentTypeCached.objects.get(model=content_instance)

    try:
        feed_object = FeedObject.objects.get(
            content_type=content_type,
            object_id=content_instance.id
        )
    except:
        return False

    return feed_object

def feed_get_or_create(content_instance):
    content_type = ContentTypeCached.objects.get(model=content_instance)

    feed_object, created = FeedObject.objects.get_or_create(
        content_type=content_type,
        object_id=content_instance.id
    )

    return feed_object

def save_feed_item(instance=None):
    feed_object = feed_get_or_create(instance)
    feed_object.save()

    return feed_object