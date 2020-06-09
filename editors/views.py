from rest_framework import generics
from editors.serializers import EditorListSerializer, EditorAddSaleSerializer
from editors.models import Editor


class EditorListView(generics.ListCreateAPIView):
    queryset = Editor.objects
    serializer_class = EditorListSerializer


class EditorDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Editor.objects
    serializer_class = EditorListSerializer


class EditorAddSaleView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Editor.objects
    serializer_class = EditorAddSaleSerializer
