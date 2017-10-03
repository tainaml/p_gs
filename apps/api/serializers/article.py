from apps.api.serializers.user import SimpleUserSerializer
from apps.article.models import Article
from rest_framework import serializers


class ArticleSerializer(serializers.ModelSerializer):

    author = SimpleUserSerializer(read_only=True)
    class Meta:
        model = Article
        fields = (
            'title',
            'text',
            'createdin',
            'publishin',
            'comment_count',
            'dislike_count',
            'like_count',
            'author'

        )
        read_only_fields = fields