import random

from django.contrib.auth import logout
from django.core.mail import send_mail
from rest_framework.generics import UpdateAPIView
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from rest_framework import status

from .models import User
from .serializers import (UserRegisterSerializer, ChangePasswordSerializer,
                          ChangeUsernameSerializer, UserResetPasswordSerializer, )


class UserRegister(APIView):
    """
        In this section, the user can register by entering his desired email username and password.
    """
    serializer_class = UserRegisterSerializer

    def post(self, request):
        ser_data = self.serializer_class(data=request.POST)
        if ser_data.is_valid():
            ser_data.create(ser_data.validated_data)
            return Response(ser_data.data, status=status.HTTP_201_CREATED)
        return Response(ser_data.errors, status=status.HTTP_400_BAD_REQUEST)


class ChangeUsername(APIView):
    """
        In this section, if the user is logged in, he can change his username
    """
    permission_classes = (IsAuthenticated,)
    serializer_class = ChangeUsernameSerializer

    def get_object(self, queryset=None):
        obj = self.request.user
        return obj

    def update(self, request, *args, **kwargs):
        user = self.get_object()
        ser_data = self.serializer_class(data=request.POST, instance=user)
        if ser_data.is_valid():
            ser_data.update(user, ser_data.validated_data)
            return Response(ser_data.data, status=status.HTTP_202_ACCEPTED)
        return Response(ser_data.errors, status=status.HTTP_400_BAD_REQUEST)


class ForgotPassword(APIView):
    """
        In this section, if the user has forgotten the password,
        enter the email and enter the password from the link sent to you
    """

    def post(self, request):
        email = request.data['email']
        if email is None:
            return Response(
                {"error": "Email is Required"},
                status=status.HTTP_422_UNPROCESSABLE_ENTITY
            )
        try:
            user = User.objects.get(email=email)
            request.session['user_id'] = user.id
            request.session['token'] = random.randint(1000, 10000)
            send_mail(
                subject="password reset token",
                message="Here is your password reset token",
                from_email="kiarashazp78@gmail.com",
                recipient_list=[user.email, ],
                html_message=f'Number reset password is : {request.session["token"]}',
            )
            return Response(status=status.HTTP_200_OK)
        except Exception as e:
            return Response(f'Exception is {e}', status=status.HTTP_400_BAD_REQUEST)


class ResetPassword(APIView):
    """
        In this section, The user enters his new password and
        if the requirements of the new password are correct for the account, he can login
    """
    serializer_class = UserResetPasswordSerializer

    def put(self, request):
        user = User.objects.get(id=request.session['user_id'])
        ser_data = self.serializer_class(data=request.POST,
                                         context={'token': request.session['token']})

        ser_data.is_valid(raise_exception=True)
        ser_data.update(user, ser_data.validated_data)
        request.session.pop('user_id')
        request.session.pop('token')
        return Response('Password changed successfully', status=status.HTTP_202_ACCEPTED)


class ChangePassword(UpdateAPIView):
    """
        In this section, the user can change password in setting profile
    """
    permission_classes = (IsAuthenticated,)

    def get_object(self, queryset=None):
        obj = self.request.user
        return obj

    def update(self, request, *args, **kwargs):
        user = self.get_object()
        ser_data = ChangePasswordSerializer(data=request.POST, context=request.user)
        if ser_data.is_valid():
            ser_data.update(user, ser_data.validated_data)
            return Response(ser_data.data, status=status.HTTP_200_OK)
        return Response(ser_data.errors, status=status.HTTP_400_BAD_REQUEST)


class UserProfile(APIView):
    """
        In this section, user seen his profile
    """
    permission_classes = [IsAuthenticated, ]

    def get(self, request):
        data_profile = {
            'username': request.user.username,
            'email': request.user.email,
            'list_wishes': {},
        }
        return Response(data_profile, status=status.HTTP_200_OK)


class UserLogout(APIView):
    """
        In this section, user logout the system
    """
    permission_classes = (IsAuthenticated,)

    def get(self, request):
        request.user.auth_token.delete()
        logout(request)
        return Response('logged out successfully', status=status.HTTP_200_OK)
