import re

from django.contrib.contenttypes.models import ContentType

from apps.core.models.embed import EmbedItem


class EmbedBusiness(object):

    EMBED_REGEX = ur'<div[^>]*data-oembed-url=["\'](.*?)["\'].*?>'

    def __init__(self, instance):
        self.instance = instance
        self.content_type = ContentType.objects.get_for_model(self.instance)

    def save(self):
        check_rule = re.compile(self.EMBED_REGEX, re.IGNORECASE)
        embeds = re.findall(check_rule, self.instance.text)

        items = []

        for embed in embeds:
            # Create or update existing items
            items.append(self.save_item(embed))

        # Get a list with atual items
        atual_items = EmbedItem.objects.filter(
            object_id=self.instance.id,
            content_type=self.content_type,
        )

        # Remove from oldest items if not present in new items.
        for atual_item in atual_items:
            if atual_item not in items:
                atual_item.delete()

    def save_item(self, item):

        embed, created = EmbedItem.objects.get_or_create(
            object_id=self.instance.id,
            content_type=self.content_type,
            embed_url=item
        )
        embed.save()
        return embed