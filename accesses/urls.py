from django.urls import path
from accesses import views


urlpatterns = (
    path('accesses/', views.AccessListView.as_view(), name='access-list'),
    path('accesses/<pk>/', views.AccessDetailView.as_view(), name='access-detail'),
)
