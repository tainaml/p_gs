
def save_feed_tags(feed_instance, data=None):

    temp_tags = data.get('tags', [])
    feed_instance.tags = temp_tags
    feed_instance.save()
    return feed_instance