from rest_framework import serializers
from networks.models import Network


class NetworkListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Network
        fields = '__all__'
