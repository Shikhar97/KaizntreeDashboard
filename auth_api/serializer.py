import six
from django.contrib.auth import authenticate
from django.contrib.sites.shortcuts import get_current_site
from django.core.mail import EmailMessage, EmailMultiAlternatives
from django.urls import reverse
from django.utils.encoding import smart_bytes, force_str
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from rest_framework import serializers
from django.contrib.auth.models import User
from rest_framework.exceptions import AuthenticationFailed
from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.auth.tokens import PasswordResetTokenGenerator
from django.utils.crypto import constant_time_compare
from django.conf import settings
from django.utils import timezone


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


class CustomPasswordResetTokenGenerator(PasswordResetTokenGenerator):
    def _make_hash_value(self, user, timestamp):
        """
        Generate a hash value that includes the user's primary key and a timestamp.
        """
        return (
                six.text_type(user.pk) + six.text_type(timestamp) +
                six.text_type(user.password)
        )

    def make_token(self, user):
        """
        Generate a token that includes the user's primary key and a timestamp with an expiry.
        """
        timestamp = str(int(timezone.now().timestamp()))  # Current timestamp
        token = self._make_hash_value(user, timestamp)
        token = token.replace("/", "")
        return f"{timestamp}-{token}"

    def check_token(self, user, token):
        """
        Check the validity of the token, including expiry check.
        """
        if not (user and token):
            return False

        # Split the token into timestamp and hash value
        try:
            timestamp, hash_value = token.split('-')
        except ValueError:
            return False

        # Check if the token has expired
        try:
            timestamp = int(timestamp)
            if timezone.now().timestamp() - timestamp > settings.PASSWORD_RESET_TIMEOUT:
                return False
        except (ValueError, TypeError):
            return False

        # Check hash value
        expected_token = self._make_hash_value(user, timestamp)
        expected_token = expected_token.replace("/", "")
        if not constant_time_compare(token, f"{timestamp}-{expected_token}"):
            return False

        return True


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
            user = User.objects.get(username=username)
            uidb64 = urlsafe_base64_encode(smart_bytes(username))
            token = CustomPasswordResetTokenGenerator().make_token(user)
            site_domain = get_current_site(self.context.get('request')).domain

            # uidb64 = 'example_uidb64'
            # token = 'example_token'

            # Generate the URL using reverse
            relative_link = reverse('reset-password-confirm', kwargs={'uidb64': uidb64, 'token': token})

            reset_link = f"http://{site_domain}{relative_link}"
            email_html_message = "Please use the link to reset the password \n\n %s" % reset_link

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


class SetNewPasswordSerializer(serializers.ModelSerializer):
    username = serializers.CharField(
        max_length=100, min_length=6, style={'class': 'shadow form-control', 'placeholder': 'Email'})
    password = serializers.CharField(max_length=100, min_length=6, write_only=True,
                                     style={'class': 'shadow form-control', 'placeholder': 'Password'})
    confirm_password = serializers.CharField(max_length=100, min_length=6, write_only=True,
                                             style={'class': 'shadow form-control', 'placeholder': 'Confirm Password'})

    class Meta:
        model = User
        fields = ['username', 'password', 'confirm_password']

    def validate(self, attrs):
        try:
            username = attrs.get('username', '')
            password = attrs.get('password', '')
            confirm_password = attrs.get('confirm_password', '')
            user = User.objects.get(username=username)

            if password != confirm_password:
                raise AuthenticationFailed("Passwords do not match")

            user.set_password(password)
            user.save()
            return user
        except Exception as e:
            raise AuthenticationFailed("Link is invalid or expired", 401)
