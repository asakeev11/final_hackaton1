from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework import generics, permissions
from rest_framework.generics import GenericAPIView
from rest_framework.filters import SearchFilter

from django.contrib.auth import get_user_model
from . import serializers
from .permission import IsAccountOwner
from car_rental.tasks import send_email_task, send_reset_password_task

User = get_user_model()


# Список юзеров может смотреть только админ
class UserListView(generics.ListAPIView):
    queryset = User.objects.all()
    filter_backends = (SearchFilter,)
    search_fields = ('email',)
    permission_classes = (permissions.IsAdminUser,)
    serializer_class = serializers.UserListSerializer


# Детальный обзор аккаунта юзера может смотреть только аутентифицированный владелец аккаунта
class UserDetailView(generics.RetrieveAPIView):
    queryset = User.objects.all()
    permission_classes = (IsAccountOwner, permissions.IsAuthenticated)
    serializer_class = serializers.UserSerializer


# Регистрироваться могут все
class RegistrationView(APIView):
    permission_classes = (permissions.AllowAny,)

    def post(self, request):
        serializer = serializers.RegisterSerializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            user = serializer.save()
            if user:
                send_email_task.delay(user.email, user.activation_code)
                return Response(serializer.data, status=201)
            return Response(status=400)


class ActivationView(APIView):
    permission_classes = (permissions.AllowAny,)

    def get(self, request, activation_code):
        try:
            user = User.objects.get(activation_code=activation_code)
            user.is_active = True
            user.activation_code = ''
            user.save()
            return Response({
                'msg': 'Successfully activated!'},
                status=200)
        except User.DoesNotExist:
            return Response({'msg': 'Link expired!'}, status=400)


class LoginApiView(TokenObtainPairView):
    serializer_class = serializers.LoginSerializer
    permission_classes = (permissions.AllowAny,)


# Выйти из аккаунта может только аутентифицированнный юзер
class LogOutApiView(GenericAPIView):
    serializer_class = serializers.LogOutSerializer
    permission_classes = (permissions.IsAuthenticated,)

    def post(self, request, *args):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response('Successfully logged out!', status=204)


class ForgotPasswordView(APIView):
    permission_classes = (permissions.AllowAny,)

    def post(self, request):
        serializer = serializers.ForgotPasswordSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        try:
            user = User.objects.get(email=serializer.data.get('email'))
            user.create_activation_code()
            user.save()
            send_reset_password_task.delay(user.email, user.activation_code)
            return Response('Check your mail', status=200)
        except User.DoesNotExist:
            return Response('User with this email does not exist', status=400)


class RestorePasswordView(APIView):
    permission_classes = (permissions.AllowAny,)

    def post(self, request):
        serializer = serializers.RestorePasswordSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response('Password changed', status=200)



