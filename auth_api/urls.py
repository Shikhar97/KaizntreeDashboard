from django.urls import path
from . import views
from .views import RegisterUser, LoginUser

urlpatterns = [
    path('login/', LoginUser.as_view()),
    path('register/', RegisterUser.as_view()),
    path('logout/', views.signout),
    path('forgotPassword/', views.forgot_password),
]