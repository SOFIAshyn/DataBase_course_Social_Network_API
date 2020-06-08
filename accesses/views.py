from rest_framework import generics
from accesses.serializers import AccessListSerializer
from accesses.models import Access


class AccessListView(generics.ListCreateAPIView):
    queryset = Access.objects
    serializer_class = AccessListSerializer


class AccessDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Access.objects
    serializer_class = AccessListSerializer

