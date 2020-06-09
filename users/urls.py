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
    path('author-in-group-size/<id>/', views.AuthorGroupSizeListView.as_view(), name='author-in-group-size'),
    path('customer-style-messages/<id>/', views.CustomerStyleListView.as_view(), name='customer-style-messages'),
    path('monthly/', views.MonthlyOrdersListView.as_view(), name='monthly-orders'),
    path('active-networks/<id>/', views.ActiveNetworksListView.as_view(), name='author-active-networks'),
    path('logged-user/', views.UserDataListView.as_view(), name='logged-in-user'),
    path('user-author-access/<customer_id>/<editor_id>/', views.UserAuthorLastAccessListView.as_view(), name='user-author-access'),
    path('author-groups/<id>/', views.AuthorGroupsListView.as_view(), name='author-groups'),
    path('authors/', views.AuthorsListView.as_view(), name='authors'),
)
