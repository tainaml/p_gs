from apps.api.serializers.user import SimpleUserSerializer
from apps.article.models import Article
from apps.feed.models import ProfileStatus
from rest_framework import serializers


class ProfileStatusSerializer(serializers.ModelSerializer):

    author = SimpleUserSerializer(read_only=True)
    class Meta:
        model = ProfileStatus
        fields = (
            'text',
            'publishin',
            'comment_count',
            'dislike_count',
            'like_count',
            'author'

        )
        read_only_fields = fields