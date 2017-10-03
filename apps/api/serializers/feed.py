from apps.api.serializers.article import ArticleSerializer
from apps.api.serializers.content_type import ContentTypeSerializer
from apps.article.models import Article
from apps.feed.models import FeedObject, ProfileStatus
from apps.question.models import Question
from rest_framework import serializers


class RelatedContentObject(serializers.RelatedField):


    def to_representation(self, value):

        if isinstance(value, Article):
            serializer = ArticleSerializer(value)
        elif isinstance(value, Question):
            serializer = ArticleSerializer(value)
        elif isinstance(value, ProfileStatus):
            serializer = ArticleSerializer(value)
        else:
            return None

        return serializer.data



class FeedObjectSerializer(serializers.ModelSerializer):



    content_object = RelatedContentObject(read_only=True)
    content_type = ContentTypeSerializer(read_only=True)
    class Meta:
        model = FeedObject
        fields = (
            "id",
            'date',
            'official',
            'content_object',
            'content_type'

        )
        read_only_fields = fields