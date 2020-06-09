from rest_framework import serializers
from editors.models import Editor


class EditorListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Editor
        fields = ('id', 'group', 'default_price', 'sale', 'sale_started')
