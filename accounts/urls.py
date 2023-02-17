from django.urls import path
from rest_framework.authtoken import views

from .views import (UserRegister, ForgotPassword, ChangePassword,
                    ChangeUsername, UserLogout, ResetPassword,
                    UserProfile, )

app_name = 'accounts'
urlpatterns = [
    path('register/', UserRegister.as_view(), name='user_register'),
    path('forgot_password/', ForgotPassword.as_view(), name='user_forgot_password'),
    path('reset_password/', ResetPassword.as_view(), name='user_reset_password'),
    path('login/', views.obtain_auth_token, name='user_login'),
    path('profile/', UserProfile.as_view(), name='user_profile'),
    path('change_password/', ChangePassword.as_view(), name='user_change_password'),
    path('change_username/', ChangeUsername.as_view(), name='user_change_username'),
    path('logout/', UserLogout.as_view(), name='user_logout'),
]
