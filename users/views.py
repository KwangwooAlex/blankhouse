from django.contrib.auth import authenticate, login, logout
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.generics import GenericAPIView

from rest_framework import status
from rest_framework.exceptions import ParseError, NotFound
from rest_framework.permissions import IsAuthenticated
import jwt
from django.conf import settings
from users.models import User
from . import serializers
import requests
from rest_framework.status import (
    HTTP_401_UNAUTHORIZED,
    HTTP_200_OK,
    HTTP_400_BAD_REQUEST,
)

from django.utils.decorators import method_decorator
from rest_framework import status
from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema
from django.contrib.auth.hashers import make_password
from rest_framework import parsers, renderers


class Me(GenericAPIView):
    permission_classes = [IsAuthenticated]

    def get_serializer_class(self, *args, **kwargs):
        if self.request.method == "GET":
            return serializers.PrivateUserSerializer
        return serializers.EditUserSerializer

    def get(self, request):
        user = request.user
        serializer = serializers.PrivateUserSerializer(user)
        return Response(serializer.data)

    def put(self, request):
        user = request.user
        serializer = serializers.EditUserSerializer(
            user,
            data=request.data,
            partial=True,
        )
        if serializer.is_valid():
            user = serializer.save()
            serializer = serializers.PrivateUserSerializer(user)
            return Response(serializer.data)
        else:
            return Response(serializer.errors)

    def delete(self, request):
        me = request.user
        me.delete()
        return Response(status=HTTP_200_OK)


class UserPassword(GenericAPIView):
    permission_classes = [IsAuthenticated]

    def get_serializer_class(self, *args, **kwargs):
        return serializers.EditPWUserSerializer

    def put(self, request):
        user = request.user
        serializer = serializers.EditPWUserSerializer(
            user,
            data=request.data,
        )
        if serializer.is_valid():
            print("encryed pw", make_password(request.data.get("password")))
            user.password = make_password(request.data.get("password"))
            user = user.save()
            serializer = serializers.PrivateUserSerializer(user)
            return Response("Password Changed")
        else:
            return Response("New Password Needed")


class Users(GenericAPIView):
    queryset = User.objects.all()  # 필수

    def get_serializer_class(self, *args, **kwargs):
        if self.request.method == "GET":
            return serializers.AllUserSerializer
        return serializers.AddUserSerializer

    def get_object(self):
        return User.objects.all()

    def get(self, request):
        if request.user.is_superuser:
            all_user = self.get_object()
            serializer = serializers.AllUserSerializer(
                all_user,
                many=True,
                context={"request": request},
            )
            return Response(serializer.data)

    def post(self, request):
        password = request.data.get("password")
        if not password:
            raise ParseError
        serializer = serializers.AddUserSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()
            user.set_password(password)  # 패스워드 관련 이것은 정해진것이다 장고 문서참고!
            # set_password 가 hashing까지 해준다
            # user.password = password (x) 이렇게하면안됨!
            user.save()
            serializer = serializers.PrivateUserSerializer(user)
            return Response(serializer.data)
        else:
            return Response(serializer.errors)


class LogIn(GenericAPIView):
    serializer_class = serializers.UserLoginSerializer

    def post(self, request):
        username = request.data.get("username")
        password = request.data.get("password")
        if not username or not password:
            raise ParseError
        user = authenticate(
            request,
            username=username,
            password=password,
        )
        if user:
            result = login(request, user)
            print("result", result)
            print("user", dir(user))
            return Response({"ok": "Welcome!"})
        else:
            return Response({"error": "wrong password"})


class LogOut(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        logout(request)
        return Response({"ok": "bye!"})
