from django.contrib.auth import authenticate
from rest_framework import serializers
from django.contrib.auth.models import User
from rest_framework.exceptions import AuthenticationFailed
from rest_framework_simplejwt.tokens import RefreshToken


def get_tokens_for_user(user):
    refresh = RefreshToken.for_user(user)
    return str(refresh), str(refresh.access_token)


# User Register serializer
class RegisterSerializer(serializers.ModelSerializer):
    password1 = serializers.CharField(max_length=20, min_length=6, write_only=True)
    password2 = serializers.CharField(max_length=20, min_length=6, write_only=True)

    class Meta:
        model = User
        fields = ['username', 'password1', 'password2']

    def validate(self, attrs):
        password1 = attrs.get('password1', '')
        password2 = attrs.get('password2', '')
        if password1 != password2:
            raise serializers.ValidationError("Passwords do not match")

        return attrs

    def create(self, validated_data):
        user = User.objects.create_user(
            username=validated_data['username'],
            password=validated_data['password1']
        )
        return user


# User Login serializer
class LoginSerializer(serializers.ModelSerializer):
    username = serializers.CharField(
        max_length=100, min_length=6, style={'class': 'shadow form-control', 'placeholder': 'Email'})
    password = serializers.CharField(
        max_length=20, write_only=True, style={'class': 'shadow form-control', 'placeholder': 'Password'})
    access_token = serializers.CharField(
        max_length=255, read_only=True)
    refresh_token = serializers.CharField(
        max_length=255, read_only=True)

    class Meta:
        model = User
        fields = ['username', 'password', 'access_token', 'refresh_token']

    def validate(self, attrs):
        username = attrs.get('username', '')
        password = attrs.get('password', '')
        request = self.context.get('request')
        user = authenticate(request, username=username, password=password)
        if not user:
            raise AuthenticationFailed("Invalid credentials, Try again")

        refresh_token, access_token = get_tokens_for_user(user)

        return {
            'username': user.username,
            'access_token': access_token,
            'refresh_token': refresh_token
        }
