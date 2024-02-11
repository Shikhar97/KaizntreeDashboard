from rest_framework import serializers
from django.contrib.auth.models import User

class UserSerializer(serializers.ModelSerializer):
    username = serializers.CharField(
        style={'class': 'shadow form-control', 'placeholder': 'Email'})
    password = serializers.CharField(
        style={'class': 'shadow form-control', 'placeholder': 'Password'})

    class Meta(object):
        model = User
        fields = ['username', 'password']
