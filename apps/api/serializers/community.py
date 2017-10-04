from apps.community.models import Community
from rest_framework import serializers


class CommunitySerializer(serializers.ModelSerializer):


    class Meta:
        model = Community
        fields = (
            'id',
            'title',
            'image'

        )
        read_only_fields = fields
