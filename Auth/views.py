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
from .models import CustomUser
from rest_framework import status


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

class UserDeletionAPIView(APIView):
    def delete(self, request):
        print(request.data)
        serializer = UserDeletionSerializer(data=request.data)
        if serializer.is_valid():
            username = serializer.validated_data['mobilenumber']
            password = serializer.validated_data['password']
            user = authenticate(request, username=username, password=password)
            if user is not None:
                user.delete()
                return Response({'message': 'User account deleted successfully.'}, status=status.HTTP_204_NO_CONTENT)
            else:
                return Response({'error': 'Invalid username or password.'}, status=status.HTTP_401_UNAUTHORIZED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

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