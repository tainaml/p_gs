from apps.userprofile.models import UserProfile
from django.contrib.auth import get_user_model
from django_thumbor import generate_url
from django.conf import settings
from rest_framework import serializers


class SimpleProfileSerializer(serializers.ModelSerializer):

    thumb = serializers.SerializerMethodField('thumborized_picture')



    def thumborized_picture(self, profile):

        return generate_url(profile.profile_picture.url, width=30, height=30) if profile.profile_picture else None

    class Meta:
        model = UserProfile
        fields = (
            'birth',
            'gender',
            'profile_picture',
            'contributor',
            'thumb'


        )
        read_only_fields = fields


class UserSerializer(serializers.ModelSerializer):

    thumb = serializers.SerializerMethodField('thumborized_picture')
    def thumborized_picture(self, user):

        return generate_url(user.profile.profile_picture.url, width=50, height=50) if user.profile and user.profile.profile_picture else None

    class Meta:
        model = get_user_model()
        fields = (
            'username',
            'id',
            'first_name',
            'last_name',
            'thumb'

        )
        read_only_fields = fields


class SimpleUserSerializer(serializers.ModelSerializer):


    profile = SimpleProfileSerializer(read_only=True)
    class Meta:
        model = get_user_model()
        fields = (
            'username',
            'id',
            'first_name',
            'last_name',
            'profile'

        )
        read_only_fields = fields

class UserProfileSerializer(serializers.ModelSerializer):


    class Meta:
        model = get_user_model()
        fields = (
            'id',
            'username',
            'first_name',
            'last_name',
            'email',


        )
        read_only_fields = ('username', 'id', 'wizard_step')

    def create(self, validated_data):

        instance = super(UserProfileSerializer, self).create(validated_data)

        return instance

    def update(self,instance, validated_data):
        instance = super(UserProfileSerializer, self).update(instance, validated_data)

        return instance

class UserWithoutEmailSerializer(UserProfileSerializer):

    class Meta:
        model = get_user_model()
        fields = (
            'id',
            'username',
            'first_name',
            'last_name',
            'email',


        )
        read_only_fields = ('username', 'id', 'wizard_step', 'email')


