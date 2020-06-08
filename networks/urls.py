from django.urls import path
from networks import views


urlpatterns = (
    path('networks/', views.NetworkListView.as_view(), name='network-list'),
    path('networks/<pk>/', views.NetworkDetailView.as_view(), name='network-detail'),
)
