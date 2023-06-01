import requests
from django.conf import settings
from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView
from rest_framework.status import HTTP_200_OK
from rest_framework.response import Response
from rest_framework.exceptions import NotFound, PermissionDenied, ParseError
from .models import Photo
from rest_framework.generics import GenericAPIView
from users.models import User
from rooms.models import Room
from experiences.models import Experience
from . import serializers
from rest_framework.status import (
    HTTP_204_NO_CONTENT,
    HTTP_400_BAD_REQUEST,
    HTTP_401_UNAUTHORIZED,
)
from rest_framework.parsers import FileUploadParser
from rest_framework import parsers, renderers


class PhotoDetail(GenericAPIView):
    queryset = Photo.objects.all()  # 필수

    permission_classes = [IsAuthenticated]

    def get_object(self, pk):
        try:
            # print("asdfasdfasfd", pk)
            return Photo.objects.get(pk=pk)
        except Photo.DoesNotExist:
            raise NotFound

    def delete(self, request, pk):
        photo = self.get_object(pk)

        photo.delete()
        return Response(status=HTTP_200_OK)


class PhotoToRoom(GenericAPIView):
    queryset = Photo.objects.all()  # 필수
    parser_classes = (
        parsers.FormParser,
        parsers.MultiPartParser,
        parsers.FileUploadParser,
    )
    renderer_classes = (renderers.JSONRenderer,)

    permission_classes = [IsAuthenticated]

    def get_serializer_class(self, *args, **kwargs):
        # 여기서는 스웨거에게 pk필수라 알려주고 post에서는 pk를받고 room을 나중에 저장해준다
        return serializers.SaveRoomPhotoSerializer

    def get_object(self, request):
        try:
            print(
                "testing room", Room.objects.get(pk=request.data.get("room_pk")).owner
            )
            print("user room", request.user)

            if (Room.objects.get(pk=request.data.get("room_pk")).owner) == (
                request.user
            ):
                return Room.objects.get(pk=request.data.get("room_pk"))
            else:
                raise ParseError("You are not the owner of it")

        except Room.DoesNotExist:
            raise NotFound

    def post(self, request, format="jpg"):
        # RealSaveRoomPhotoSerializer
        serializer = serializers.RealSaveRoomPhotoSerializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            room = self.get_object(request)
            print("roomroomroom", room)
            data = serializer.save(room=room)
            # resume.name - file name
            # resume.read() - file contens
            return Response({"success": "True"})
        return Response({"success": "False"}, status=HTTP_400_BAD_REQUEST)


class PhotoToExperience(GenericAPIView):
    queryset = Photo.objects.all()  # 필수
    parser_classes = (
        parsers.FormParser,
        parsers.MultiPartParser,
        parsers.FileUploadParser,
    )
    renderer_classes = (renderers.JSONRenderer,)

    permission_classes = [IsAuthenticated]

    def get_serializer_class(self, *args, **kwargs):
        # 여기서는 스웨거에게 pk필수라 알려주고 post에서는 pk를받고 room을 나중에 저장해준다
        return serializers.SaveExperiencePhotoSerializer

    def get_object(self, request):
        try:
            if (Experience.objects.get(pk=request.data.get("experience_pk")).host) == (
                request.user
            ):
                return Experience.objects.get(pk=request.data.get("experience_pk"))
            else:
                raise ParseError("You are not the host of it")

        except Experience.DoesNotExist:
            raise NotFound

    def post(self, request, format="jpg"):
        # RealSaveRoomPhotoSerializer
        serializer = serializers.RealSaveExperiencePhotoSerializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            experience = self.get_object(request)
            print("experienceexperienceexperience", experience)
            data = serializer.save(experience=experience)
            # resume.name - file name
            # resume.read() - file contens
            return Response({"success": "True"})
        return Response({"success": "False"}, status=HTTP_400_BAD_REQUEST)


class UserAvatar(GenericAPIView):
    queryset = Photo.objects.all()  # 필수
    parser_classes = (
        parsers.FormParser,
        parsers.MultiPartParser,
        parsers.FileUploadParser,
    )
    renderer_classes = (renderers.JSONRenderer,)

    permission_classes = [IsAuthenticated]

    def get_serializer_class(self, *args, **kwargs):
        return serializers.SaveUserAvatarSerializer

    def get_object(self, request):
        try:
            return User.objects.get(pk=request.user.pk)
        except User.DoesNotExist:
            raise NotFound

    def post(self, request, format="jpg"):
        user = self.get_object(request)
        if Photo.objects.filter(user=request.user).exists():
            user.avatar.delete()

        serializer = serializers.SaveUserAvatarSerializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            print("useruseruser", user)
            serializer.save(user=user)
            # resume.name - file name
            # resume.read() - file contens
            return Response({"success": "True"})
        return Response({"success": "False"}, status=HTTP_400_BAD_REQUEST)

    # def put(self, request, format="jpg"):
    #     serializer = serializers.SaveUserAvatarSerializer(data=request.data)
    #     if serializer.is_valid(raise_exception=True):
    #         user = self.get_object(request)
    #         print("useruseruser", user)
    #         serializer.save(user=user)
    #         # resume.name - file name
    #         # resume.read() - file contens
    #         return Response({"success": "True"})
    #     return Response({"success": "False"}, status=HTTP_400_BAD_REQUEST)
