from django.contrib.auth import logout
from django.core.mail import EmailMultiAlternatives
from django.template.loader import get_template
from rest_framework.decorators import api_view, authentication_classes, permission_classes
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.response import Response
from rest_framework import status
from django.contrib import auth

from django.shortcuts import get_object_or_404, render
from django.contrib.auth.models import User
from rest_framework.authtoken.models import Token

from .reset import password_reset_token_created
from .serializer import UserSerializer


@api_view(['POST'])
@permission_classes([AllowAny])
def register(request):
    serializer = UserSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()
        user = User.objects.get(username=request.data['username'])
        user.set_password(request.data['password'])
        user.save()
        auth.login(request=request, user=user)
        serializer = UserSerializer(user)
        token, created = Token.objects.get_or_create(user=user)
        return Response({'token': token.key, 'user': serializer.data}, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['POST'])
@permission_classes([AllowAny])
def login(request):
    user = auth.authenticate(username=request.data['username'], password=request.data['password'])
    if user is not None:
        auth.login(request=request, user=user)
        serializer = UserSerializer(user)
        token, created = Token.objects.get_or_create(user=user)
        return Response({'token': token.key, 'user': serializer.data}, status=status.HTTP_200_OK)
    else:
        return Response({'error': 'Wrong username or password'}, status=status.HTTP_403_FORBIDDEN)


@api_view(['POST'])
@permission_classes([AllowAny])
def forgot_password(request):
    password_reset_token_created()
    htmly = get_template('account/email.html')
    d = {'username': request.data['username']}
    subject, from_email, to = 'Password Reset', 'no-reply@kaizn.com', request.data['username']
    html_content = htmly.render(d)
    # 'reset_password_url': "{}?token={}".format(
    #     instance.request.build_absolute_uri(reverse('password_reset:reset-password-confirm')),
    #     reset_password_token.key)
    msg = EmailMultiAlternatives(subject, html_content, from_email, [to])
    msg.attach_alternative(html_content, "text/html")
    msg.send()
    return Response({'message': 'Password reset email sent.'}, status=status.HTTP_200_OK)
