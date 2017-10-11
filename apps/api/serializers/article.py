from apps.api.serializers.community import CommunitySerializer
from apps.api.serializers.content_type import ContentTypeSerializer
from apps.api.serializers.user import SimpleUserSerializer
from apps.article.models import Article
from apps.feed.models import FeedObject
from django.template.defaultfilters import striptags
from django_thumbor import generate_url
from rest_framework import serializers


class SimpleFeedObjectSerializer(serializers.ModelSerializer):


    communities = CommunitySerializer(many=True)
    class Meta:
        model = FeedObject
        fields = (
            "id",
            'date',
            'official',
            "communities"

        )
        read_only_fields = fields

class ArticleSerializer(serializers.ModelSerializer):

    author = SimpleUserSerializer(read_only=True)
    image = serializers.SerializerMethodField('get_abs_image')
    feed = SimpleFeedObjectSerializer(read_only=True, many=True)

    def get_abs_image(self, obj):


        return generate_url(obj.image.url, width=800, height=600) if obj.image and hasattr(obj.image, 'url') else None


    class Meta:
        model = Article
        fields = (
            "id",
            'title',
            'text',
            'createdin',
            'image',
            'publishin',
            'comment_count',
            'dislike_count',
            'like_count',
            'author',
            "feed"

        )
        read_only_fields = fields


class SimpleArticleSerializer(serializers.ModelSerializer):

    author = SimpleUserSerializer(read_only=True)
    image = serializers.SerializerMethodField('get_abs_image')

    text = serializers.SerializerMethodField('get_partial_text')

    def get_partial_text(self, obj):
        return striptags(obj.text[:100])  + "..."

    def get_abs_image(self, obj):


        return generate_url(obj.image.url, width=800, height=600) if obj.image and hasattr(obj.image, 'url') else None


    class Meta:
        model = Article
        fields = (
            'title',
            'text',
            'createdin',
            'image',
            'publishin',
            'comment_count',
            'dislike_count',
            'like_count',
            'author'

        )
        read_only_fields = fields