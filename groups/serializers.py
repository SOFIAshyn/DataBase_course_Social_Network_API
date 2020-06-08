from rest_framework import serializers
from groups.models import Group
from django.contrib.auth import get_user_model

User = get_user_model()


class ShortUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('username', )


class GroupListSerializer(serializers.ModelSerializer):
    participants_count = serializers.SerializerMethodField()
    participants = ShortUserSerializer(many=True, required=False)

    class Meta:
        model = Group
        fields = ('id', 'name', 'participants_count', 'participants')

    def get_participants_count(self, obj):
        return obj.participants.count()
