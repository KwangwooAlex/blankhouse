from django.shortcuts import render
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticatedOrReadOnly
from .models import Amenity, Room
from rest_framework.views import APIView
from rest_framework.status import (
    HTTP_204_NO_CONTENT,
    HTTP_400_BAD_REQUEST,
    HTTP_401_UNAUTHORIZED,
)
from . import serializers
from rest_framework.exceptions import (
    NotFound,
    NotAuthenticated,
    ParseError,
    PermissionDenied,
)
from rest_framework.generics import GenericAPIView
from django.db import transaction
from drf_yasg.utils import swagger_auto_schema
from bookings.models import Booking
from bookings.serializers import PublicBookingSerializer, CreateRoomBookingSerializer
from django.utils import timezone
from django.utils.decorators import method_decorator
from drf_yasg import openapi

# Create your views here.


class RoomDetail(GenericAPIView):
    queryset = Room.objects.all()  # 필수
    permission_classes = [IsAuthenticatedOrReadOnly]

    def get_serializer_class(self, *args, **kwargs):
        # if self.request.method == "PUT":
        #     return serializers.ProductDetailEditSerializer
        return serializers.RoomDetailSerializer

    def get_object(self, pk):
        try:
            return Room.objects.get(pk=pk)
        except Room.DoesNotExist:
            raise NotFound

    def get(self, request, pk):
        Room = self.get_object(pk)

        serializer = serializers.RoomDetailSerializer(
            Room,
            context={"request": request},
        )
        return Response(serializer.data)


class Amenities(GenericAPIView):
    queryset = Amenity.objects.all()  # 필수
    permission_classes = [
        IsAuthenticatedOrReadOnly
    ]  # 유저검사 get은허용 delete put post는 유저인증된사라만 가능! 다른기능은 없음

    def get_serializer_class(self, *args, **kwargs):
        return serializers.AmenitySerializer

    @swagger_auto_schema(
        # request_body=serializers.EditAmenitySerializer,
        tags=["Amenities"],
        operation_id="This is testing api ID 111",
        operation_summary="This is swagger description testing text",
        operation_description="Modify Amenity detail",
        # deprecated=True,
    )
    def get(self, request):
        all_room_categories = Amenity.objects.all()
        serializer = serializers.AmenitySerializer(
            all_room_categories,
            many=True,
            context={"request": request},
            # 여기의 context를 이용하여 원하는 메소드 어떤것이든 시리얼라이저의
            # context에 접근할수있음
        )
        return Response(serializer.data)

    @swagger_auto_schema(
        # request_body=serializers.EditAmenitySerializer,
        tags=["Amenities"],
        operation_id="This is testing api ID 1222",
        operation_summary="This is swagger description testing text",
        operation_description="Modify Amenity detail",
        # deprecated=True,
    )
    def post(self, request):
        serializer = serializers.AmenitySerializer(data=request.data)
        if serializer.is_valid():
            try:
                with transaction.atomic():  # transaction 써줘야 만들다가 실패하면 rollback함
                    newAmenity = serializer.save()
                    serializer = serializers.AmenitySerializer(
                        newAmenity,
                        context={"request": request},
                    )

                return Response(serializer.data)
            except Exception:
                # transaction 이 실패하면 에러를 낼것임
                raise ParseError(
                    "product not found, check backend cart view and search!!"
                )

        else:
            return Response(
                serializer.errors,
                status=HTTP_400_BAD_REQUEST,
            )


class RoomBookings(GenericAPIView):
    queryset = Room.objects.all()  # 필수
    permission_classes = [IsAuthenticatedOrReadOnly]

    def get_serializer_class(self, *args, **kwargs):
        if self.request.method == "POST":
            return CreateRoomBookingSerializer
        return PublicBookingSerializer

    def get_object(self, pk):
        try:
            return Room.objects.get(pk=pk)
        except:
            raise NotFound

    def get(self, request, pk):
        room = self.get_object(pk)
        now = timezone.localtime(timezone.now()).date()
        bookings = Booking.objects.filter(
            room=room,
            kind=Booking.BookingKindChoices.ROOM,
            check_in__gt=now,  # 현재보다 미래의 예약만 보여주고 싶음!
        )
        serializer = PublicBookingSerializer(bookings, many=True)
        return Response(serializer.data)

    def post(self, request, pk):
        room = self.get_object(pk)
        serializer = CreateRoomBookingSerializer(
            data=request.data,
            context={"room": room},
        )
        if serializer.is_valid():
            booking = serializer.save(
                room=room,
                user=request.user,
                kind=Booking.BookingKindChoices.ROOM,
            )
            serializer = PublicBookingSerializer(booking)
            return Response(serializer.data)
        else:
            return Response(
                serializer.errors,
                status=HTTP_400_BAD_REQUEST,
            )


@method_decorator(
    name="get",
    decorator=swagger_auto_schema(
        manual_parameters=[
            openapi.Parameter(
                "check_in",
                openapi.IN_QUERY,
                description="check in time ex) 2023-06-06",
                type=openapi.TYPE_STRING,
            ),
            openapi.Parameter(
                "check_out",
                openapi.IN_QUERY,
                description="check out time ex) 2023-06-06",
                type=openapi.TYPE_STRING,
            ),
        ]
    ),
)
class RoomBookingCheck(GenericAPIView):
    queryset = Room.objects.all()  # 필수
    permission_classes = [IsAuthenticatedOrReadOnly]

    def get_serializer_class(self, *args, **kwargs):
        if self.request.method == "GET":
            return CreateRoomBookingSerializer
        # return PublicBookingSerializer

    def get_object(self, pk):
        try:
            return Room.objects.get(pk=pk)
        except:
            raise NotFound

    def get(self, request, pk):
        room = self.get_object(pk)
        check_in = request.query_params.get("check_in")
        check_out = request.query_params.get("check_out")
        print("check IN", check_in)
        exists = Booking.objects.filter(
            room=room,
            check_in__lt=check_out,
            check_out__gt=check_in,
        ).exists()
        if exists:
            return Response({"ok": False})
        return Response({"ok": True})


class AmenityDetail(GenericAPIView):
    queryset = Amenity.objects.all()  # 필수

    permission_classes = [
        IsAuthenticatedOrReadOnly
    ]  # 유저검사 get은허용 delete put post는 유저인증된사라만 가능! 다른기능은 없음

    def get_serializer_class(self, *args, **kwargs):
        if self.request.method == "PUT":
            return serializers.EditAmenitySerializer

    def get_object(self, pk):
        try:
            return Amenity.objects.get(pk=pk)
        except Amenity.DoesNotExist:
            raise NotFound

    @swagger_auto_schema(
        # request_body=serializers.EditAmenitySerializer,
        tags=["Amenities"],
        operation_id="This is testing api ID 22222",
        operation_summary="This is swagger description testing text",
        operation_description="Modify Amenity detail",
        # deprecated=True,
    )
    def put(self, request, pk):
        if request.user.is_superuser:
            amenity = self.get_object(pk)
            serializer = serializers.EditAmenitySerializer(
                amenity,
                data=request.data,
                partial=True,  # 부분적으로만 업데이트 허용!
            )
            # save() 는 update or create 중 알아서 serializer가 메소드를 이다음 실행시켜줌
            if serializer.is_valid():
                updated_amenity = serializer.save()
                return Response(
                    serializers.AmenitySerializer(updated_amenity).data,
                )
            else:
                return Response(
                    serializer.errors,
                    status=HTTP_400_BAD_REQUEST,
                )

    @swagger_auto_schema(
        # request_body=serializers.EditAmenitySerializer,
        tags=["Amenities"],
        operation_id="This is testing api ID 3333",
        operation_summary="This is swagger description testing text",
        operation_description="Modify Amenity detail",
        # deprecated=True,
    )
    def delete(self, request, pk):
        amenity = self.get_object(pk)

        if request.user.is_superuser == False:
            raise PermissionDenied

        amenity.delete()

        return Response(status=HTTP_204_NO_CONTENT)
