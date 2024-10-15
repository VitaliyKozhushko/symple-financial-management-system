"""
Модуль с роутами для пользователей
"""
from django.urls import path
from .views import UserListView, UserDetailView

urlpatterns = [
    path('users/', UserListView.as_view(), name='user-list-create'),
    path('users/<int:pk>/', UserDetailView.as_view(), name='user-detail-update-delete'),
]
