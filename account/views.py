from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from rest_framework.authtoken.admin import User

from .forms import SignupForm, LoginForm
from django.contrib import messages

from rest_framework.decorators import api_view, authentication_classes, permission_classes
from rest_framework.authentication import SessionAuthentication, TokenAuthentication
from django.contrib.sessions.middleware import SessionMiddleware
from django.utils.timezone import now
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.response import Response
from rest_framework import status
from django.contrib import auth
from django.views.decorators.csrf import ensure_csrf_cookie, csrf_protect, csrf_exempt
from django.utils.decorators import method_decorator

from django.shortcuts import get_object_or_404
from django.contrib.auth.models import User
from rest_framework.authtoken.models import Token

from django.views.decorators.csrf import ensure_csrf_cookie
from django.http import JsonResponse


def index(request):
    return render(request, 'account/login.html')


def user_signup(request):
    if request.method == 'POST':
        form = SignupForm(request.POST, request.FILES)
        if form.is_valid():
            user = form.save()
            login(request, user)
            token, created = Token.objects.get_or_create(user=user)
            print(token, created)
            return redirect('home_page')
    else:
        form = SignupForm()
    return render(request, 'account/signup.html', {'form': form})


def user_login(request):
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            user = authenticate(request, username=username, password=password)
            if user:
                login(request, user)
                token, created = Token.objects.get_or_create(user=user)
                print(token, created)
                return redirect('home_page')
            else:
                return render(request, 'account/login.html', {'form': form, 'message': "Wrong username or password"})
        return render(request, 'account/login.html', {'form': form, 'message': form.errors})
    else:
        form = LoginForm()
    return render(request, 'account/login.html', {'form': form})


def user_logout(request):
    logout(request)
    return redirect('login')


def home_page(request):
    # patient_data = request.user

    return render(request, 'item_dashboard/table.html')
