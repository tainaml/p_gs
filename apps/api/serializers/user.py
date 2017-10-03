
from django.contrib.auth import get_user_model

from rest_framework import serializers


class UserSerializer(serializers.ModelSerializer):

    class Meta:
        model = get_user_model()
        fields = (
            'username',
            'id',
            'first_name',
            'last_name',

        )
        read_only_fields = ('username', 'id',)


class SimpleUserSerializer(serializers.ModelSerializer):

    class Meta:
        model = get_user_model()
        fields = (
            'username',
            'id',
            'first_name',
            'last_name',

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


