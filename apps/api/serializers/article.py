from apps.api.serializers.user import SimpleUserSerializer
from apps.article.models import Article
from django_thumbor import generate_url
from rest_framework import serializers


class ArticleSerializer(serializers.ModelSerializer):

    author = SimpleUserSerializer(read_only=True)
    image = serializers.SerializerMethodField('get_abs_image')

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