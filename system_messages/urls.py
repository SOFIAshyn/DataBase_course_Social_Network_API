from django.urls import path
from system_messages import views


urlpatterns = (
    path('system_messages/', views.SystemMessageListView.as_view(), name='message-list'),
    path('system_messages/<pk>/', views.SystemMessageDetailView.as_view(), name='message-detail'),
)
