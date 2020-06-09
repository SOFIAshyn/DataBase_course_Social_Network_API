from rest_framework import serializers
from editors.models import Editor
from drf_writable_nested.serializers import WritableNestedModelSerializer
from drf_writable_nested.mixins import UniqueFieldsMixin, NestedUpdateMixin


class EditorListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Editor
        fields = ('id', 'group', 'default_price', 'sale', 'sale_started')
        extra_kwargs = {"sale_started": {"allow_null": True}}


class EditorAddSaleSerializer(WritableNestedModelSerializer):
    class Meta:
        model = Editor
        fields = ('sale', 'sale_started')