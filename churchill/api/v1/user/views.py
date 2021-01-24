from django.contrib.auth import authenticate
from django.db.utils import IntegrityError
from rest_framework import status
from rest_framework.authtoken.models import Token
from rest_framework.generics import CreateAPIView
from rest_framework.permissions import AllowAny
from rest_framework.response import Response

from churchill.api.v1.user.serializers import (
    RegisterSerializer,
    LoginSerializer,
    RegisterVerifySerializer,
    ResetPasswordSerializer,
    ResetPasswordConfirmSerializer,
)
from churchill.apps.users.services import (
    create_user,
    send_verification_email,
    verify_user,
    send_reset_password_email,
    reset_user_password,
)


class RegisterView(CreateAPIView):
    permission_classes = (AllowAny,)
    serializer_class = RegisterSerializer

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        try:
            user = create_user(**serializer.validated_data)
            send_verification_email(user)
        except IntegrityError:
            return Response(status=status.HTTP_409_CONFLICT)
        return Response(status=status.HTTP_201_CREATED)


class RegisterVerifyView(CreateAPIView):
    permission_classes = (AllowAny,)
    serializer_class = RegisterVerifySerializer

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        if not verify_user(**serializer.validated_data):
            return Response(status=status.HTTP_400_BAD_REQUEST)
        return Response()


class LoginView(CreateAPIView):
    permission_classes = (AllowAny,)
    serializer_class = LoginSerializer

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = authenticate(
            username=serializer.validated_data["email"],
            password=serializer.validated_data["password"],
        )
        if user is None:
            return Response(status=status.HTTP_404_NOT_FOUND)
        token, _ = Token.objects.get_or_create(user=user)
        return Response({"token": token.key}, status=status.HTTP_201_CREATED)


class ResetPasswordView(CreateAPIView):
    permission_classes = (AllowAny,)
    serializer_class = ResetPasswordSerializer

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        if not send_reset_password_email(**serializer.validated_data):
            Response(status=status.HTTP_400_BAD_REQUEST)
        return Response(status=status.HTTP_201_CREATED)


class ResetPasswordConfirmView(CreateAPIView):
    permission_classes = (AllowAny,)
    serializer_class = ResetPasswordConfirmSerializer

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        if not reset_user_password(**serializer.validated_data):
            return Response(status=status.HTTP_400_BAD_REQUEST)
        return Response()
