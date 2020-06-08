from django.urls import path
from users import views


urlpatterns = (
    path('users/', views.UserListView.as_view(), name='user-list'),
    path('users/<pk>/', views.UserDetailView.as_view(), name='user-detail'),
    path('customers/<id>/', views.CustomerListView.as_view(), name='author-customers'),
    path('authors/<id>/', views.AuthorListView.as_view(), name='customer-authors'),
    path('author-of-diff-customers/', views.AuthorOfDiffCustomersListView.as_view(), name='author-of-diff-customers'),
    path('customers-of-diff-messages/', views.CustomerOfDiffMessagesListView.as_view(), name='customers-of-diff-messages'),
    path('socials/<id>/', views.SocialsListView.as_view(), name='customers-socials'),
    path('authors-socials/<id>/', views.AuthorsSocialsListView.as_view(), name='authors-socials'),
    path('authors-denied/<id>/', views.AccessDeniedListView.as_view(), name='authors-permission-denied'),
    path('author-customer/<author_id>/<customer_id>/', views.CommonEventsListView.as_view(), name='author-customer'),
)
