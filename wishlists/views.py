from rest_framework.views import APIView
from rest_framework.status import HTTP_200_OK
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rooms.models import Room
from experiences.models import Experience
from .models import Wishlist
from .serializers import RoomWishlistSerializer, ExperienceWishlistSerializer
from rest_framework.exceptions import (
    NotFound,
    NotAuthenticated,
    ParseError,
    PermissionDenied,
)
from rest_framework.generics import GenericAPIView
from . import serializers


class RoomWishlists(GenericAPIView):
    queryset = Wishlist.objects.all()
    permission_classes = [IsAuthenticated]

    def get_serializer_class(self, *args, **kwargs):
        if self.request.method == "PUT":
            return serializers.SaveRoomWishlistSerializer
        return serializers.RoomWishlistSerializer

    def get_object(self, request):
        try:
            return Wishlist.objects.get(user=request.user)
        except Wishlist.DoesNotExist:
            raise ParseError("No wishlist")

    def get(self, request):
        try:
            wishlist = Wishlist.objects.get(user=request.user)
            serializer = RoomWishlistSerializer(
                wishlist,
                context={"request": request},
            )
            return Response(serializer.data)
        except Wishlist.DoesNotExist:
            raise ParseError("No wishlist")

    def get_room(self, pk):
        try:
            return Room.objects.get(pk=pk)
        except Room.DoesNotExist:
            raise NotFound

    # 좋아하는방을 넣기위해서는 add로 해야한다!
    def put(self, request):
        # print("product_pkproduct_pk", product_pk)
        # 없으면 만들고 바로 넣는다
        if Wishlist.objects.filter(user=request.user).exists() == False:
            serializer = RoomWishlistSerializer(data=request.data)
            if serializer.is_valid():
                wishlist = serializer.save(
                    user=request.user,
                )
                serializer = RoomWishlistSerializer(wishlist)

        wishlist = self.get_object(request)
        room = self.get_room(request.data.get("room_pk"))
        if wishlist.rooms.filter(pk=room.pk).exists():
            wishlist.rooms.remove(room)
        else:
            wishlist.rooms.add(room)
        return Response(status=HTTP_200_OK)


class ExperienceWishlists(GenericAPIView):
    queryset = Wishlist.objects.all()
    permission_classes = [IsAuthenticated]

    def get_serializer_class(self, *args, **kwargs):
        if self.request.method == "PUT":
            return serializers.SaveExperienceWishlistSerializer
        return serializers.ExperienceWishlistSerializer

    def get_object(self, request):
        try:
            return Wishlist.objects.get(user=request.user)
        except Wishlist.DoesNotExist:
            raise ParseError("No wishlist")

    def get(self, request):
        try:
            wishlist = Wishlist.objects.get(user=request.user)
            serializer = ExperienceWishlistSerializer(
                wishlist,
                #  many=True, 이건 행을 여러개 불러올때.. 이건 하나의 행에 여러개의 일일투어가 포함되어있는것임
                context={"request": request},
            )
            return Response(serializer.data)
        except Wishlist.DoesNotExist:
            raise ParseError("No wishlist")

    def get_experience(self, pk):
        try:
            return Experience.objects.get(pk=pk)
        except Experience.DoesNotExist:
            raise NotFound

    # 좋아하는방을 넣기위해서는 add로 해야한다!
    def put(self, request):
        # print("product_pkproduct_pk", product_pk)
        # 없으면 만들고 바로 넣는다
        if Wishlist.objects.filter(user=request.user).exists() == False:
            serializer = ExperienceWishlistSerializer(data=request.data)
            if serializer.is_valid():
                wishlist = serializer.save(
                    user=request.user,
                )
                serializer = ExperienceWishlistSerializer(wishlist)

        wishlist = self.get_object(request)
        experience = self.get_experience(request.data.get("experience_pk"))
        if wishlist.experiences.filter(pk=experience.pk).exists():
            wishlist.experiences.remove(experience)
        else:
            wishlist.experiences.add(experience)
        return Response(status=HTTP_200_OK)
