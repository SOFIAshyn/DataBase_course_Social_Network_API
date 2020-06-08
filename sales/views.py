from rest_framework import generics
from sales.serializers import SaleListSerializer
from sales.models import Sale


class SaleListView(generics.ListCreateAPIView):
    queryset = Sale.objects
    serializer_class = SaleListSerializer


class SaleDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Sale.objects
    serializer_class = SaleListSerializer
