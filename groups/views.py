from django.shortcuts import render

# Create your views here.
from rest_framework import generics
from groups.serializers import GroupListSerializer, GroupInsertAuthorSerializer
from groups.models import Group
from rest_framework.views import APIView
from editors.models import Editor
from editors.serializers import EditorIdSerializer
from rest_framework.response import Response


class GroupListView(generics.ListCreateAPIView):
    queryset = Group.objects
    serializer_class = GroupListSerializer


class GroupDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Group.objects
    serializer_class = GroupListSerializer


class GroupInsertUserView(generics.RetrieveUpdateAPIView):
    queryset = Group.objects
    serializer_class = GroupInsertAuthorSerializer


class GroupEditorView(APIView):
    def get(self, request, id=None):
        group_editor = Editor.objects.filter(group=id)

        serializer = EditorIdSerializer(group_editor, many=True)
        return Response(serializer.data, status=200)




