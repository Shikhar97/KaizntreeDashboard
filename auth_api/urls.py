from django.urls import path
from .views import RegisterUser, LoginUser, ResetPassword, PasswordResetConfirm, Logout

urlpatterns = [
    path('login/', LoginUser.as_view(), name='login'),
    path('register/', RegisterUser.as_view(), name='register'),
    path('reset-password-confirm/<uidb64>/<token>/', PasswordResetConfirm.as_view(), name='reset-password-confirm'),
    path('reset_password/', ResetPassword.as_view(), name='reset-password'),
    path("logout/", Logout.as_view(), name='logout'),
]