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

class ForgotPasswordAPIView(APIView):
    def post(self, request):
        serializer = ForgotPasswordSerializer(data=request.data)
        if serializer.is_valid():
            mobile_number = serializer.validated_data['mobile_number']
            user = User.objects.filter(profile__mobile_number=mobile_number).first()  # Adjust the filtering based on your user model setup
            if user:
                # Generate and send password reset instructions via SMS
                # Example: Generate a random OTP and send it to the provided mobile number using an SMS API
                # Replace the following lines with your SMS sending logic
                reset_code = '123456'  # Example reset code
                # Send SMS logic here

                return Response({'message': 'Password reset code sent successfully'})
            else:
                return Response({'error': 'User with this mobile number does not exist'}, status=400)
        return Response(serializer.errors, status=400)
    
class ResetPasswordAPIView(APIView):
    def post(self, request):
        serializer = ResetPasswordSerializer(data=request.data)
        if serializer.is_valid():
            mobile_number = serializer.validated_data['mobile_number']
            reset_code = serializer.validated_data['reset_code']
            new_password = serializer.validated_data['new_password']
            
            user_profile = CustomUser.objects.filter(mobile_number=mobile_number).first()
            if user_profile:
                # Validate the reset code here (you can save the reset code in the UserProfile model)
                if user_profile.reset_code == reset_code:
                    user = user_profile.user
                    user.set_password(new_password)
                    user.save()
                    
                    # Optionally, reset the reset code to null/empty after password change
                    user_profile.reset_code = None
                    user_profile.save()
                    
                    return Response({'message': 'Password reset successful'})
                else:
                    return Response({'error': 'Invalid reset code'}, status=400)
            else:
                return Response({'error': 'User with this mobile number does not exists'})

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