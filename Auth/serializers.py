from rest_framework import serializers
from django.contrib.auth import get_user_model
from rest_framework.authtoken.models import Token

User = get_user_model()

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'first_name']

class RegistrationSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['username', 'password', 'first_name','last_name']
        extra_kwargs = {'password': {'write_only': True}}

    def create(self, validated_data):
        user = User.objects.create_user(**validated_data)
        Token.objects.create(user=user)
        return user

class ForgotPasswordSerializer(serializers.Serializer):
    mobile_number = serializers.CharField(max_length=15)


class ResetPasswordSerializer(serializers.Serializer):
    mobile_number = serializers.CharField(max_length=10)
    reset_code = serializers.CharField(max_length=6)  
    new_password = serializers.CharField(max_length=128) 