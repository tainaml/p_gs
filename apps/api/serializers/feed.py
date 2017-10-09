from apps.api.serializers.article import ArticleSerializer
from apps.api.serializers.community import CommunitySerializer
from apps.api.serializers.content_type import ContentTypeSerializer
from apps.api.serializers.profilestatus import ProfileStatusSerializer
from apps.api.serializers.question import QuestionSerializer
from apps.article.models import Article
from apps.feed.models import FeedObject, ProfileStatus
from apps.question.models import Question
from rest_framework import serializers


class RelatedContentObject(serializers.RelatedField):


    def to_representation(self, value):
        request =  self.context['request']
        if isinstance(value, Article):
            serializer = ArticleSerializer(value, context={'request': request})
        elif isinstance(value, Question):
            serializer = QuestionSerializer(value, context={'request': request})
        elif isinstance(value, ProfileStatus):
            serializer = ProfileStatusSerializer(value, context={'request': request})
        else:
            return None

        return serializer.data



class FeedObjectSerializer(serializers.ModelSerializer):



    content_object = RelatedContentObject(read_only=True)
    content_type = ContentTypeSerializer(read_only=True)
    communities = CommunitySerializer(many=True)
    class Meta:
        model = FeedObject
        fields = (
            "id",
            'date',
            'official',
            'content_object',
            'content_type',
            "communities"

        )
        read_only_fields = fields