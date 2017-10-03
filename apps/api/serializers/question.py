from apps.api.serializers.user import SimpleUserSerializer
from apps.question.models import Question
from rest_framework import serializers


class QuestionSerializer(serializers.ModelSerializer):

    author = SimpleUserSerializer(read_only=True)
    class Meta:
        model = Question
        fields = (
            'title',
            'description',
            'question_date',
            'like_count',
            'dislike_count',
            'comment_count',
            'author'

        )
        read_only_fields = fields