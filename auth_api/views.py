from django.core.mail import EmailMultiAlternatives
from django.template.loader import get_template
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status, generics
from django.contrib import auth

from auth_api.serializer import RegisterSerializer, LoginSerializer, PasswordResetSerializer


class RegisterUser(generics.GenericAPIView):
    serializer_class = RegisterSerializer

    def post(self, request, *args, **kwargs):
        register_serializer = RegisterSerializer(data=request.data)
        if register_serializer.is_valid(raise_exception=True):
            register_serializer.save()
            return Response({"user": register_serializer.data, "message": "User Created Successfully"},
                            status=status.HTTP_201_CREATED)
        return Response(register_serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class LoginUser(generics.GenericAPIView):
    serializer_class = LoginSerializer

    def post(self, request, *args, **kwargs):
        login_serializer = LoginSerializer(data=request.data, context={'request': request})
        if login_serializer.is_valid(raise_exception=True):
            return Response(login_serializer.data, status=status.HTTP_200_OK)
        return Response(login_serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class ResetPassword(generics.GenericAPIView):
    serializer_class = PasswordResetSerializer

    def post(self, request, *args, **kwargs):
        reset_serializer = PasswordResetSerializer(data=request.data)
        if reset_serializer.is_valid(raise_exception=True):
            return Response({'message': 'Password reset email sent.'}, status=status.HTTP_200_OK)
        return Response(reset_serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class Logout(generics.GenericAPIView):

    def get(self, request):
        request.user.auth_token.delete()
        auth.logout(request)
        return Response("Logout successful", status=status.HTTP_200_OK)
