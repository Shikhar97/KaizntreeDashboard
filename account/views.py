from django.contrib import auth
from rest_framework.decorators import api_view, authentication_classes, permission_classes
from rest_framework.authentication import SessionAuthentication, TokenAuthentication
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.response import Response
from rest_framework import status

from django.shortcuts import get_object_or_404
from django.contrib.auth.models import User
from rest_framework.authtoken.models import Token

from .serializer import UserSerializer

from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from .forms import UserCreationForm, LoginForm


# Home page
def index(request):
    return render(request, 'account/login.html')


# # signup page
# def user_signup(request):
#     if request.method == 'POST':
#         form = UserCreationForm(request.POST)
#         if form.is_valid():
#             form.save()
#             return redirect('login')
#     else:
#         form = UserCreationForm()
#     return render(request, 'account/signup.html', {'form': form})
#
#
# # login page
# def user_login(request):
#     if request.method == 'POST':
#         form = LoginForm(request.POST)
#         if form.is_valid():
#             username = form.cleaned_data['username']
#             password = form.cleaned_data['password']
#             user = authenticate(request, username=username, password=password)
#             if user:
#                 login(request, user)
#                 return redirect('home')
#     else:
#         form = LoginForm()
#     return render(request, 'account/login.html', {'form': form})


# @api_view(['POST'])
# def user_signup(request):
#     if request.method == 'POST':
#         serializer = UserSerializer(data=request.data)
#         if serializer.is_valid():
#             serializer.save()
#             user = User.objects.get(username=request.data['username'])
#             user.set_password(request.data['password'])
#             user.save()
#             token = Token.objects.create(user=user)
#             return Response({'token': token.key, 'user': serializer.data}, status=status.HTTP_201_CREATED)
#         return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
#     return render(request, 'account/signup.html')
#
#
# @api_view(['POST'])
# def user_login(request):
#     if request.method == 'POST':
#         user = get_object_or_404(User, username=request.data['username'])
#         if not user.check_password(request.data['password']):
#             return Response('User is not registered', status=status.HTTP_404_NOT_FOUND)
#         token, created = Token.objects.get_or_create(user=user)
#         serializer = UserSerializer(user)
#         return render(request, 'account/login.html', Response({'token': token.key, 'user': serializer.data}, status=status.HTTP_200_OK))
#     return render(request, 'account/login.html')
#
#
# @api_view(['GET'])
# @authentication_classes([SessionAuthentication, TokenAuthentication])
# @permission_classes([IsAuthenticated])
# def testtoken(request):
#     return Response('Token authenticated successfully')
#
#
# # logout page
# def user_logout(request):
#     logout(request)
#     return redirect('login')
#
#


@api_view(['POST'])
@permission_classes([AllowAny])
def signup(request):
    serializer = UserSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()
        user = User.objects.get(username=request.data['username'])
        user.set_password(request.data['password'])
        user.save()
        return Response({'user': serializer.data}, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST, template_name='account/signup.html')


@api_view(['POST'])
@permission_classes([AllowAny])
def login(request):
    user = auth.authenticate(username=request.data['username'], password=request.data['password'])
    # if not user.check_password(request.data['password']):
    #     return Response('User is not registered', status=status.HTTP_404_NOT_FOUND)
    if user is not None:
        auth.login(request=request, user=user)
        serializer = UserSerializer(user)
        return Response({'user': serializer.data}, status=status.HTTP_200_OK)
    else:
        return Response(status=status.HTTP_404_NOT_FOUND, template_name='account/login.html')


@api_view(['POST'])
@permission_classes([AllowAny])
def forgotpassword(request):
    user = get_object_or_404(User, email=request.data['email'])
    serializer = UserSerializer(user)
    return Response("Password reset email sent.", status=status.HTTP_200_OK)

