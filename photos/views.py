import requests
from django.conf import settings
from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView
from rest_framework.status import HTTP_200_OK
from rest_framework.response import Response
from rest_framework.exceptions import NotFound, PermissionDenied
from .models import Photo
from rest_framework.generics import GenericAPIView
from users.models import User
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


# class PhotoToProduct(GenericAPIView):
#     queryset = Photo.objects.all()  # 필수
#     parser_classes = (
#         parsers.FormParser,
#         parsers.MultiPartParser,
#         parsers.FileUploadParser,
#     )
#     renderer_classes = (renderers.JSONRenderer,)

#     permission_classes = [IsAuthenticated]

#     def get_serializer_class(self, *args, **kwargs):
#         return serializers.SaveUserAvatarSerializer

#     def get_object(self, request):
#         try:
#             return User.objects.get(user=request.user)
#         except User.DoesNotExist:
#             raise NotFound

#     def post(self, request, pk, format="jpg"):
#         serializer = serializers.SaveUserAvatarSerializer(data=request.data)
#         if serializer.is_valid(raise_exception=True):
#             user = self.get_object(request)
#             data = serializer.save(product=product)
#             # resume.name - file name
#             # resume.read() - file contens
#             return Response({"success": "True"})
#         return Response({"success": "False"}, status=HTTP_400_BAD_REQUEST)


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
