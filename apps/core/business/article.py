from apps.feed.service import business as BusinessFeed


def save_feed_item(article, data=None):
    feed_object = BusinessFeed.feed_get_or_create(article)
    feed_object.date = article.publishin if article.is_published() else None
    feed_object.save()
    return feed_object
