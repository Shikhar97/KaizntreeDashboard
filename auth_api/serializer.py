from django.contrib.auth import authenticate
from django.core.mail import EmailMessage, EmailMultiAlternatives
from django.urls import reverse
from django.utils.encoding import smart_bytes
from django.utils.http import urlsafe_base64_encode
from rest_framework import serializers
from django.contrib.auth.models import User
from rest_framework.exceptions import AuthenticationFailed
from rest_framework_simplejwt.tokens import RefreshToken

from kaizntree_dashboard import settings


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
        username = attrs.get('username', '')

        if User.objects.filter(username=username).exists():
            raise serializers.ValidationError("Username already exists")

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

        if not User.objects.filter(username=username).exists():
            raise serializers.ValidationError("Username dosen't exists")

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


# Password Reset serializer
class PasswordResetSerializer(serializers.ModelSerializer):
    username = serializers.CharField(
        max_length=100, min_length=6, style={'class': 'shadow form-control', 'placeholder': 'Email'})

    class Meta:
        model = User
        fields = ['username']

    def validate(self, attrs):
        username = attrs.get('username', '')

        if not User.objects.filter(username=username).exists():
            raise serializers.ValidationError("Username dosen't exists")
        else:
            uidb64 = urlsafe_base64_encode(smart_bytes(username))
            # send an e-mail to the user
            context = {
                'current_user': username,
                'username': username,
                'email': username,
                'reset_password_url': "{}?token={}".format(
                    self.context.get('request').build_absolute_uri(reverse('reset_password')),
                    uidb64)
            }
            # render email text
            email_html_message = "Please use the link to reset the password \n\n %s" % context["reset_password_url"]

            msg = EmailMultiAlternatives(
                # title:
                "Password Reset",
                # message:
                email_html_message,
                # from:
                settings.EMAIL_HOST_USER,
                # to:
                [username]
            )
            msg.send()
        return super().validate(attrs)
