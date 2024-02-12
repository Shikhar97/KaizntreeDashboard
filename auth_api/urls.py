from django.urls import path
from .views import RegisterUser, LoginUser, ResetPassword

urlpatterns = [
    path('login/', LoginUser.as_view()),
    path('register/', RegisterUser.as_view()),
    path('reset_password/', ResetPassword.as_view()),
]