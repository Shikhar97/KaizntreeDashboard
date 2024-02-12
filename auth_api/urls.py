from django.urls import path
from .views import RegisterUser, LoginUser, ResetPassword

urlpatterns = [
    path('login/', LoginUser.as_view(), name='login'),
    path('register/', RegisterUser.as_view(), name='register'),
    path('reset_password/', ResetPassword.as_view(), name='reset_password'),
]