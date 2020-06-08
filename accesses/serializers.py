from rest_framework import serializers
from accesses.models import Access
from system_messages.serializers import SystemMessageListSerializer


class AccessListSerializer(serializers.ModelSerializer):

    class Meta:
        model = Access
        fields = ('id', 'social_name', 'customer', 'editor', 'date_start', 'date_end')


class AccessMessageListSerializer(serializers.ModelSerializer):

    messages = SystemMessageListSerializer(many=True, read_only=True)

    class Meta:
        model = Access
        fields = ('id', 'social_name', 'customer', 'editor', 'date_start', 'date_end', 'messages')

