from rest_framework import generics
from networks.models import Network
from networks.serializers import NetworkListSerializer


class NetworkListView(generics.ListCreateAPIView):
    queryset = Network.objects
    serializer_class = NetworkListSerializer


class NetworkDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Network.objects
    serializer_class = NetworkListSerializer

