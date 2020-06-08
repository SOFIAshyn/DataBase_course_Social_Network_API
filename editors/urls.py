from django.urls import path
from editors import views


urlpatterns = (
    path('editors/', views.EditorListView.as_view(), name='editor-list'),
    path('editors/<pk>/', views.EditorDetailView.as_view(), name='editor-detail'),
)
