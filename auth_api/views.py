from django.utils.encoding import smart_str, DjangoUnicodeDecodeError
from django.utils.http import urlsafe_base64_decode
from django_rest_passwordreset.views import User
from rest_framework.response import Response
from rest_framework import status, generics
from django.contrib import auth

from auth_api.serializer import RegisterSerializer, LoginSerializer, PasswordResetSerializer, \
    CustomPasswordResetTokenGenerator, SetNewPasswordSerializer


class RegisterUser(generics.GenericAPIView):
    serializer_class = RegisterSerializer

    def post(self, request, *args, **kwargs):
        register_serializer = RegisterSerializer(data=request.data)
        if register_serializer.is_valid(raise_exception=True):
            register_serializer.save()
            return Response(register_serializer.data,
                            status=status.HTTP_201_CREATED)
        return Response(register_serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class LoginUser(generics.GenericAPIView):
    serializer_class = LoginSerializer

    def post(self, request, *args, **kwargs):
        try:
            login_serializer = LoginSerializer(data=request.data, context={'request': request})
            if login_serializer.is_valid(raise_exception=True):
                return Response(login_serializer.data, status=status.HTTP_200_OK)
        except Exception as e:
            if "invalid" in str(e).lower() or "username" in str(e).lower():
                return Response(str(e), status=status.HTTP_401_UNAUTHORIZED)
            return Response(str(e), status=status.HTTP_400_BAD_REQUEST)


class ResetPassword(generics.GenericAPIView):
    serializer_class = PasswordResetSerializer

    def post(self, request, *args, **kwargs):
        reset_serializer = PasswordResetSerializer(data=request.data, context={'request': request})
        if reset_serializer.is_valid(raise_exception=True):
            return Response({'message': 'Password reset email sent.'}, status=status.HTTP_200_OK)
        return Response(reset_serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class PasswordResetConfirm(generics.GenericAPIView):
    serializer_class = SetNewPasswordSerializer

    def get(self, request, uidb64, token):
        try:
            user_id = smart_str(urlsafe_base64_decode(uidb64))
            user = User.objects.get(username=user_id)
            if not CustomPasswordResetTokenGenerator().check_token(user, token):
                return Response({"message": "Token is invalid or has expired"}, status.HTTP_401_UNAUTHORIZED)
            return Response({'success': True, 'message': "Credentials are valid", 'uidb64': uidb64, 'token': token},
                            status=status.HTTP_200_OK)
        except DjangoUnicodeDecodeError:
            return Response({"message": "Token is invalid or has expired"}, status.HTTP_401_UNAUTHORIZED)

    def patch(self, request, *args, **kwargs):
        new_password_serializer = SetNewPasswordSerializer(data=request.data, context={'request': request})
        new_password_serializer.is_valid(raise_exception=True)
        return Response({"message": "Password Reset Successful"}, status=status.HTTP_200_OK)


class Logout(generics.GenericAPIView):

    def get(self, request):
        request.user.auth_token.delete()
        auth.logout(request)
        return Response("Logout successful", status=status.HTTP_200_OK)
