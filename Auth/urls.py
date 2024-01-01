from django.urls import path
from .views import UserListView, RegistrationAPIView, LoginAPIView
urlpatterns = [
    path('users/', UserListView.as_view(), name='user-list'),
    path('register/', RegistrationAPIView.as_view(), name='register'),
    path('login/', LoginAPIView.as_view(), name='login'),

]
