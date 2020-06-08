from rest_framework import generics
from system_messages.models import SystemMessage
from system_messages.serializers import SystemMessageListSerializer


class SystemMessageListView(generics.ListCreateAPIView):
    queryset = SystemMessage.objects
    serializer_class = SystemMessageListSerializer


class SystemMessageDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = SystemMessage.objects
    serializer_class = SystemMessageListSerializer

