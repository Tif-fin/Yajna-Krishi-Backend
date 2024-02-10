from django.urls import path
from .views import UserListView, RegistrationAPIView, LoginAPIView, get_user_info, delete_user
urlpatterns = [
    path('users/', UserListView.as_view(), name='user-list'),
    path('register/', RegistrationAPIView.as_view(), name='register'),
    path('login/', LoginAPIView.as_view(), name='login'),
    path('user-info/', get_user_info, name='user_info'),
    path('delete/', delete_user, name='delete_user_api'),
]
