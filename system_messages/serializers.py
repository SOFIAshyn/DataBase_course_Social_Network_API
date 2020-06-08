from rest_framework import serializers
from system_messages.models import SystemMessage


class SystemMessageListSerializer(serializers.ModelSerializer):
    class Meta:
        model = SystemMessage
        fields = ('id', 'style', 'access', 'date', 'text')
