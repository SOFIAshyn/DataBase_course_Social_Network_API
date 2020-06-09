from django.shortcuts import render

# Create your views here.
from rest_framework import generics
from groups.serializers import GroupListSerializer, GroupInsertAuthorSerializer
from groups.models import Group


class GroupListView(generics.ListCreateAPIView):
    queryset = Group.objects
    serializer_class = GroupListSerializer


class GroupDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Group.objects
    serializer_class = GroupListSerializer


class GroupInsertUserView(generics.RetrieveUpdateAPIView):
    queryset = Group.objects
    serializer_class = GroupInsertAuthorSerializer



