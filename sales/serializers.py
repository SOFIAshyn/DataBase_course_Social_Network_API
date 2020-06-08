from rest_framework import serializers
from sales.models import Sale


class SaleListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Sale
        fields = ('id', 'percent', 'duration')
