from django.urls import path
from groups import views


urlpatterns = (
    path('groups/', views.GroupListView.as_view(), name='group-list'),
    path('groups/<pk>/', views.GroupDetailView.as_view(), name='group-detail'),
    path('groups-insert/<pk>/', views.GroupInsertUserView.as_view(), name='group-insert'),
)
