from django.shortcuts import render

# Create your views here.
from rest_framework import generics
from groups.serializers import GroupListSerializer
from groups.models import Group


class GroupListView(generics.ListCreateAPIView):
    queryset = Group.objects
    serializer_class = GroupListSerializer


class GroupDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Group.objects
    serializer_class = GroupListSerializer

