from rest_framework import serializers
from groups.models import Group
from django.contrib.auth import get_user_model
from drf_writable_nested.serializers import WritableNestedModelSerializer

User = get_user_model()


class ShortUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('id', 'username')
        extra_kwargs = {"username": {"required": False}}


class GroupListSerializer(serializers.ModelSerializer):
    participants_count = serializers.SerializerMethodField()
    participants = ShortUserSerializer(many=True, required=False)

    class Meta:
        model = Group
        fields = ('id', 'name', 'participants_count', 'participants')

    def get_participants_count(self, obj):
        return obj.participants.count()


class GroupInsertAuthorSerializer(WritableNestedModelSerializer):
    participants = ShortUserSerializer(many=True, required=False)

    class Meta:
        model = Group
        fields = ('id', 'name', 'participants')
        read_only_fields = ('id', 'name')
