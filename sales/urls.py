from django.urls import path
from sales import views


urlpatterns = (
    path('sales/', views.SaleListView.as_view(), name='sales-list'),
    path('sales/<pk>/', views.SaleDetailView.as_view(), name='sale-detail'),
)
