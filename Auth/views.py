# myapp/views.py

from rest_framework import generics
from rest_framework.response import Response
from rest_framework.authtoken.models import Token
from django.contrib.auth import get_user_model
from .serializers import *
from django.contrib.auth import authenticate, login
from rest_framework.views import APIView
from rest_framework.permissions import AllowAny
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.authentication import TokenAuthentication
from rest_framework.decorators import api_view, permission_classes, authentication_classes
from django.contrib.auth.models import User
from django.contrib.auth import authenticate
from django.shortcuts import render, redirect
from django.contrib import messages
from .forms import UserDeletionForm

User = get_user_model()

class UserListView(generics.ListAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer

class RegistrationAPIView(generics.CreateAPIView):
    queryset = User.objects.all()
    serializer_class = RegistrationSerializer
    permission_classes = [AllowAny]

class LoginAPIView(APIView):
    permission_classes = [AllowAny]

    def post(self, request, *args, **kwargs):
        data = request.data
        username = data.get('username', None)
        password = data.get('password', None)

        user = authenticate(username=username, password=password)

        if user is not None:
            # login(request, user)
            token, created = Token.objects.get_or_create(user=user)
            return Response({'token': token.key})
        else:
            return Response({'error': 'Invalid credentials'})

def delete_user(request):
    if request.method == 'POST':
        form = UserDeletionForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['mobilenumber']
            password = form.cleaned_data['password']
            user = authenticate(request, username=username, password=password)
            if user is not None:
                user.delete()
                messages.success(request, 'Your account has been deleted successfully.')
                return render(request, 'html/deletion_success.html')
            else:
                messages.error(request, 'Invalid username or password.')
    else:
        form = UserDeletionForm()
    return render(request, 'html/deletion.html', {'form': form})

def privacy_policy(request):
    return render(request, 'html/privacy_policy.html')

@api_view(['GET'])
@permission_classes([IsAuthenticated])
@authentication_classes([TokenAuthentication])
def get_user_info(request):
    user = request.user  
    user_info = {
        'first_name': user.first_name,
        'last_name': user.last_name,
        'mobile': user.username
    }
    return Response(user_info)