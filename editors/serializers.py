from rest_framework import serializers
from editors.models import Editor


class EditorListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Editor
        fields = '__all__'
